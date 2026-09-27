from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.prescription import Prescription, PrescriptionItem
from app.models.patient import Patient
from app.models.medical_record import MedicalRecord
from app.models.appointment import Appointment
from datetime import datetime, date

prescription_bp = Blueprint('prescription', __name__)


@prescription_bp.route('/')
@login_required
def list_prescriptions():
    if current_user.is_admin():
        prescriptions_list = Prescription.query.order_by(Prescription.prescription_date.desc()).all()
    elif current_user.is_doctor():
        prescriptions_list = Prescription.query.filter_by(
            doctor_id=current_user.doctor_profile.id
        ).order_by(Prescription.prescription_date.desc()).all()
    elif current_user.is_patient():
        prescriptions_list = Prescription.query.filter_by(
            patient_id=current_user.patient_profile.id
        ).order_by(Prescription.prescription_date.desc()).all()
    else:
        prescriptions_list = []
    return render_template('prescriptions/list.html', prescriptions=prescriptions_list)


@prescription_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not (current_user.is_admin() or current_user.is_doctor()):
        flash('غير مصرح لك بتحرير وصفات دوائية. Access denied.', 'danger')
        return redirect(url_for('prescription.list_prescriptions'))

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        medical_record_id = request.form.get('medical_record_id') or None
        prescription_date = request.form.get('prescription_date')
        instructions = request.form.get('instructions', '').strip()

        medicine_names = request.form.getlist('medicine_name')
        dosages = request.form.getlist('dosage')
        frequencies = request.form.getlist('frequency')
        durations = request.form.getlist('duration')
        item_instructions = request.form.getlist('item_instructions')

        errors = []
        if not all([patient_id, prescription_date]):
            errors.append('يرجى تحديد المريض وتاريخ الوصفة الطبية.')
        if not medicine_names or not any(m.strip() for m in medicine_names):
            errors.append('يجب إضافة صنف دوائي واحد على الأقل.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return redirect(url_for('prescription.create'))

        doctor_id = current_user.doctor_profile.id if current_user.is_doctor() else request.form.get('doctor_id')
        date_obj = datetime.strptime(prescription_date, '%Y-%m-%d').date()

        prescription = Prescription(
            patient_id=int(patient_id),
            doctor_id=int(doctor_id),
            medical_record_id=int(medical_record_id) if medical_record_id else None,
            prescription_date=date_obj,
            instructions=instructions
        )
        db.session.add(prescription)
        db.session.flush()

        for i, name in enumerate(medicine_names):
            if name.strip():
                item = PrescriptionItem(
                    prescription_id=prescription.id,
                    medicine_name=name.strip(),
                    dosage=dosages[i].strip() if i < len(dosages) else '',
                    frequency=frequencies[i].strip() if i < len(frequencies) else '',
                    duration=durations[i].strip() if i < len(durations) else '',
                    instructions=item_instructions[i].strip() if i < len(item_instructions) else ''
                )
                db.session.add(item)

        db.session.commit()
        flash('تم تحرير الوصفة الطبية وحفظها بنجاح!', 'success')
        return redirect(url_for('prescription.detail', prescription_id=prescription.id))

    if current_user.is_doctor():
        doctor = current_user.doctor_profile
        patient_ids = db.session.query(Appointment.patient_id).filter_by(
            doctor_id=doctor.id
        ).distinct().all()
        patient_ids = [p[0] for p in patient_ids]
        patients_list = Patient.query.filter(Patient.id.in_(patient_ids)).all()
        records_list = MedicalRecord.query.filter_by(
            doctor_id=doctor.id
        ).order_by(MedicalRecord.visit_date.desc()).all()
    else:
        patients_list = Patient.query.all()
        records_list = MedicalRecord.query.order_by(MedicalRecord.visit_date.desc()).all()

    return render_template('prescriptions/create.html',
                           patients=patients_list,
                           records=records_list,
                           today=date.today().isoformat())


@prescription_bp.route('/<int:prescription_id>')
@login_required
def detail(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    if current_user.is_patient():
        if prescription.patient_id != current_user.patient_profile.id:
            flash('غير مصرح لك بالاطلاع على هذه الوصفة. Access denied.', 'danger')
            return redirect(url_for('prescription.list_prescriptions'))
    elif current_user.is_doctor():
        if prescription.doctor_id != current_user.doctor_profile.id:
            flash('غير مصرح لك بالاطلاع على هذه الوصفة. Access denied.', 'danger')
            return redirect(url_for('prescription.list_prescriptions'))
    return render_template('prescriptions/detail.html', prescription=prescription)
