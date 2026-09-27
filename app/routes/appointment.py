from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.user import User
from datetime import datetime, date

appointment_bp = Blueprint('appointment', __name__)


@appointment_bp.route('/')
@login_required
def list_appointments():
    if current_user.is_admin():
        appointments_list = Appointment.query.order_by(Appointment.appointment_date.desc()).all()
    elif current_user.is_doctor():
        appointments_list = Appointment.query.filter_by(
            doctor_id=current_user.doctor_profile.id
        ).order_by(Appointment.appointment_date.desc()).all()
    elif current_user.is_patient():
        appointments_list = Appointment.query.filter_by(
            patient_id=current_user.patient_profile.id
        ).order_by(Appointment.appointment_date.desc()).all()
    else:
        appointments_list = []
    return render_template('appointments/list.html', appointments=appointments_list)


@appointment_bp.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    if request.method == 'POST':
        # For patient accounts, strictly bind to their own profile ID
        if current_user.is_patient():
            patient_id = current_user.patient_profile.id
        else:
            patient_id = request.form.get('patient_id')

        doctor_id = request.form.get('doctor_id')
        appt_date = request.form.get('appointment_date')
        appt_time = request.form.get('appointment_time')
        reason = request.form.get('reason', '').strip()
        duration = int(request.form.get('duration', 30))

        errors = []
        if not all([patient_id, doctor_id, appt_date, appt_time]):
            errors.append('يرجى ملء جميع الحقول الإلزامية المطلوبة.')

        if not errors:
            try:
                appt_date_obj = datetime.strptime(appt_date, '%Y-%m-%d').date()
                appt_time_obj = datetime.strptime(appt_time, '%H:%M').time()
            except ValueError:
                errors.append('صيغة التاريخ أو وقت الموعد غير صحيحة.')
                appt_date_obj = None
                appt_time_obj = None

            if not errors:
                if appt_date_obj < date.today():
                    errors.append('لا يمكن حجز موعد في تاريخ سابق. Cannot book in past.')

                # Check Doctor Working Hours
                doctor = db.session.get(Doctor, int(doctor_id)) or Doctor.query.get(int(doctor_id))
                if doctor and doctor.working_start_time and doctor.working_end_time:
                    if appt_time_obj < doctor.working_start_time or appt_time_obj >= doctor.working_end_time:
                        errors.append(
                            f'الوقت المحدد ({appt_time}) خارج فترة دوام د. {doctor.user.full_name} ({doctor.working_hours_arabic}). يرجى اختيار موعد ضمن فترة الدوام.'
                        )

                existing = Appointment.query.filter_by(
                    doctor_id=int(doctor_id),
                    appointment_date=appt_date_obj,
                    appointment_time=appt_time_obj,
                    status='Scheduled'
                ).first()
                if existing:
                    errors.append('هذا الموعد محجوز مسبقاً لدى الطبيب المحدد. Slot already booked.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            doctors_list = Doctor.query.join(User).filter(Doctor.is_available.is_(True)).all()
            patients_list = Patient.query.join(User).all()
            return render_template('appointments/book.html',
                                   doctors=doctors_list,
                                   patients=patients_list,
                                   selected_patient_id=int(patient_id) if patient_id else None,
                                   today=date.today().isoformat())

        appointment = Appointment(
            patient_id=int(patient_id),
            doctor_id=int(doctor_id),
            appointment_date=appt_date_obj,
            appointment_time=appt_time_obj,
            duration_minutes=duration,
            reason=reason,
            status='Scheduled'
        )
        db.session.add(appointment)
        db.session.commit()
        flash('تم تأكيد حجز الموعد بنجاح!', 'success')
        return redirect(url_for('appointment.list_appointments'))

    doctors_list = Doctor.query.join(User).filter(Doctor.is_available.is_(True)).all()
    patients_list = Patient.query.join(User).all()

    selected_patient_id = None
    if current_user.is_patient():
        selected_patient_id = current_user.patient_profile.id

    return render_template('appointments/book.html',
                           doctors=doctors_list,
                           patients=patients_list,
                           selected_patient_id=selected_patient_id,
                           today=date.today().isoformat())


@appointment_bp.route('/<int:appt_id>')
@login_required
def detail(appt_id):
    appointment = db.session.get(Appointment, appt_id) or Appointment.query.get_or_404(appt_id)

    if current_user.is_patient():
        if appointment.patient_id != current_user.patient_profile.id:
            flash('غير مصرح لك بالاطلاع على هذا الموعد. Access denied.', 'danger')
            return redirect(url_for('appointment.list_appointments'))
    elif current_user.is_doctor():
        if appointment.doctor_id != current_user.doctor_profile.id:
            flash('غير مصرح لك بالاطلاع على هذا الموعد. Access denied.', 'danger')
            return redirect(url_for('appointment.list_appointments'))

    return render_template('appointments/detail.html', appointment=appointment)


@appointment_bp.route('/<int:appt_id>/cancel', methods=['POST'])
@login_required
def cancel(appt_id):
    appointment = db.session.get(Appointment, appt_id) or Appointment.query.get_or_404(appt_id)

    if appointment.status == 'Completed':
        flash('لا يمكن إلغاء موعد مكتمل بالفعل.', 'warning')
        return redirect(url_for('appointment.detail', appt_id=appt_id))

    if current_user.is_patient():
        if appointment.patient_id != current_user.patient_profile.id:
            flash('غير مصرح لك بإلغاء هذا الموعد. Access denied.', 'danger')
            return redirect(url_for('appointment.list_appointments'))
    elif current_user.is_doctor():
        if appointment.doctor_id != current_user.doctor_profile.id:
            flash('غير مصرح لك بإلغاء هذا الموعد. Access denied.', 'danger')
            return redirect(url_for('appointment.list_appointments'))

    appointment.status = 'Cancelled'
    db.session.commit()
    flash('تم إلغاء الموعد بنجاح.', 'info')
    return redirect(url_for('appointment.list_appointments'))


@appointment_bp.route('/<int:appt_id>/complete', methods=['POST'])
@login_required
def complete(appt_id):
    if not (current_user.is_admin() or current_user.is_doctor()):
        flash('غير مصرح لك بتغيير حالة هذا الموعد. Access denied.', 'danger')
        return redirect(url_for('appointment.list_appointments'))

    appointment = db.session.get(Appointment, appt_id) or Appointment.query.get_or_404(appt_id)
    appointment.status = 'Completed'
    db.session.commit()
    flash('تم تحديث حالة الموعد إلى مكتمل بنجاح!', 'success')
    return redirect(url_for('appointment.detail', appt_id=appt_id))
