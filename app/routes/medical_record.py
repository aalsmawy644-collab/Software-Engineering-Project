from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.medical_record import MedicalRecord
from app.models.patient import Patient
from app.models.appointment import Appointment
from datetime import datetime, date

medical_record_bp = Blueprint('medical_record', __name__)


@medical_record_bp.route('/')
@login_required
def list_records():
    if current_user.is_admin():
        records = MedicalRecord.query.order_by(MedicalRecord.visit_date.desc()).all()
    elif current_user.is_doctor():
        records = MedicalRecord.query.filter_by(
            doctor_id=current_user.doctor_profile.id
        ).order_by(MedicalRecord.visit_date.desc()).all()
    elif current_user.is_patient():
        records = MedicalRecord.query.filter_by(
            patient_id=current_user.patient_profile.id
        ).order_by(MedicalRecord.visit_date.desc()).all()
    else:
        records = []
    return render_template('medical_records/list.html', records=records)


@medical_record_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if not (current_user.is_admin() or current_user.is_doctor()):
        flash('غير مصرح لك بإنشاء تقارير طبية. Access denied.', 'danger')
        return redirect(url_for('medical_record.list_records'))

    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        appointment_id = request.form.get('appointment_id') or None
        visit_date = request.form.get('visit_date')
        chief_complaint = request.form.get('chief_complaint', '').strip()
        diagnosis = request.form.get('diagnosis', '').strip()
        treatment_plan = request.form.get('treatment_plan', '').strip()
        notes = request.form.get('notes', '').strip()
        follow_up_date = request.form.get('follow_up_date') or None

        errors = []
        if not all([patient_id, visit_date, chief_complaint, diagnosis]):
            errors.append('يرجى تعبئة الحقول الإلزامية: المريض، تاريخ الكشف، الشكوى، والتشخيص الطبي.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return redirect(url_for('medical_record.create'))

        doctor_id = current_user.doctor_profile.id if current_user.is_doctor() else request.form.get('doctor_id')
        visit_date_obj = datetime.strptime(visit_date, '%Y-%m-%d').date()
        follow_up_obj = datetime.strptime(follow_up_date, '%Y-%m-%d').date() if follow_up_date else None

        record = MedicalRecord(
            patient_id=int(patient_id),
            doctor_id=int(doctor_id),
            appointment_id=int(appointment_id) if appointment_id else None,
            visit_date=visit_date_obj,
            chief_complaint=chief_complaint,
            diagnosis=diagnosis,
            treatment_plan=treatment_plan,
            notes=notes,
            follow_up_date=follow_up_obj
        )
        db.session.add(record)
        db.session.commit()
        flash('تم تسجيل التقرير الطبي وحفظه بنجاح!', 'success')
        return redirect(url_for('medical_record.detail', record_id=record.id))

    if current_user.is_doctor():
        doctor = current_user.doctor_profile
        patient_ids = db.session.query(Appointment.patient_id).filter_by(
            doctor_id=doctor.id
        ).distinct().all()
        patient_ids = [p[0] for p in patient_ids]
        patients_list = Patient.query.filter(Patient.id.in_(patient_ids)).all()
        appointments_list = Appointment.query.filter_by(
            doctor_id=doctor.id, status='Completed'
        ).all()
    else:
        patients_list = Patient.query.all()
        appointments_list = Appointment.query.filter_by(status='Completed').all()

    return render_template('medical_records/create.html',
                           patients=patients_list,
                           appointments=appointments_list,
                           today=date.today().isoformat())


@medical_record_bp.route('/<int:record_id>')
@login_required
def detail(record_id):
    record = MedicalRecord.query.get_or_404(record_id)
    if current_user.is_patient():
        if record.patient_id != current_user.patient_profile.id:
            flash('غير مصرح لك بالاطلاع على هذا التقرير. Access denied.', 'danger')
            return redirect(url_for('medical_record.list_records'))
    elif current_user.is_doctor():
        if record.doctor_id != current_user.doctor_profile.id:
            flash('غير مصرح لك بالاطلاع على هذا التقرير. Access denied.', 'danger')
            return redirect(url_for('medical_record.list_records'))
    return render_template('medical_records/detail.html', record=record)
