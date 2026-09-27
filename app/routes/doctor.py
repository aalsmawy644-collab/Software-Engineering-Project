from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.medical_record import MedicalRecord
from datetime import date, datetime, time

doctor_bp = Blueprint('doctor', __name__)


def doctor_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_doctor():
            flash('غير مصرح لك بالدخول. هذه الصفحة مخصصة للأطباء فقط. Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@doctor_bp.route('/dashboard')
@login_required
@doctor_required
def dashboard():
    doctor = current_user.doctor_profile
    today = date.today()
    todays_appointments = Appointment.query.filter_by(
        doctor_id=doctor.id, appointment_date=today
    ).all()
    scheduled_appointments = Appointment.query.filter_by(
        doctor_id=doctor.id, status='Scheduled'
    ).count()
    total_patients_seen = db.session.query(Appointment.patient_id).filter_by(
        doctor_id=doctor.id, status='Completed'
    ).distinct().count()
    recent_records = MedicalRecord.query.filter_by(
        doctor_id=doctor.id
    ).order_by(MedicalRecord.created_at.desc()).limit(5).all()
    return render_template('doctor/dashboard.html',
                           doctor=doctor,
                           todays_appointments=todays_appointments,
                           scheduled_appointments=scheduled_appointments,
                           total_patients_seen=total_patients_seen,
                           recent_records=recent_records)


@doctor_bp.route('/appointments')
@login_required
@doctor_required
def appointments():
    doctor = current_user.doctor_profile
    status_filter = request.args.get('status', '')
    query = Appointment.query.filter_by(doctor_id=doctor.id)
    if status_filter:
        query = query.filter_by(status=status_filter)
    appointments_list = query.order_by(
        Appointment.appointment_date.desc(), Appointment.appointment_time.desc()
    ).all()
    return render_template('doctor/appointments.html',
                           appointments=appointments_list,
                           status_filter=status_filter)


@doctor_bp.route('/appointments/<int:appt_id>/complete', methods=['POST'])
@login_required
@doctor_required
def complete_appointment(appt_id):
    doctor = current_user.doctor_profile
    appt = Appointment.query.filter_by(id=appt_id, doctor_id=doctor.id).first_or_404()
    appt.status = 'Completed'
    db.session.commit()
    flash('تم إنهاء الكشف وتحديث حالة الموعد إلى مكتمل بنجاح.', 'success')
    return redirect(url_for('doctor.appointments'))


@doctor_bp.route('/patients')
@login_required
@doctor_required
def patients():
    doctor = current_user.doctor_profile
    patient_ids = db.session.query(Appointment.patient_id).filter_by(
        doctor_id=doctor.id
    ).distinct().all()
    patient_ids = [p[0] for p in patient_ids]
    patients_list = Patient.query.filter(Patient.id.in_(patient_ids)).all()
    return render_template('doctor/patients.html', patients=patients_list)


@doctor_bp.route('/profile')
@login_required
@doctor_required
def profile():
    doctor = current_user.doctor_profile
    return render_template('doctor/profile.html', doctor=doctor)


@doctor_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
@doctor_required
def edit_profile():
    doctor = current_user.doctor_profile
    user = current_user
    if request.method == 'POST':
        user.first_name = request.form.get('first_name', user.first_name).strip()
        user.last_name = request.form.get('last_name', user.last_name).strip()
        user.phone = request.form.get('phone', '').strip()
        doctor.bio = request.form.get('bio', '').strip()
        
        fee = request.form.get('consultation_fee')
        if fee:
            try:
                doctor.consultation_fee = float(fee)
            except ValueError:
                pass

        start_time_str = request.form.get('working_start_time', '')
        end_time_str = request.form.get('working_end_time', '')
        if start_time_str:
            try:
                doctor.working_start_time = datetime.strptime(start_time_str, '%H:%M').time()
            except ValueError:
                pass
        if end_time_str:
            try:
                doctor.working_end_time = datetime.strptime(end_time_str, '%H:%M').time()
            except ValueError:
                pass

        doctor.is_available = 'is_available' in request.form

        new_password = request.form.get('new_password', '')
        if new_password:
            user.set_password(new_password)
        db.session.commit()
        flash('تم تحديث بيانات الملف الشخصي وساعات الدوام بنجاح!', 'success')
        return redirect(url_for('doctor.profile'))
    return render_template('doctor/edit_profile.html', doctor=doctor)
