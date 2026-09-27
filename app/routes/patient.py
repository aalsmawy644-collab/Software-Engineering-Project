from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app.models.appointment import Appointment
from app.models.medical_record import MedicalRecord
from app.models.prescription import Prescription
from datetime import date

patient_bp = Blueprint('patient', __name__)


def patient_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_patient():
            flash('Access denied. Patient privileges required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@patient_bp.route('/dashboard')
@login_required
@patient_required
def dashboard():
    patient = current_user.patient_profile
    today = date.today()
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.appointment_date >= today,
        Appointment.status == 'Scheduled'
    ).order_by(Appointment.appointment_date, Appointment.appointment_time).limit(5).all()
    medical_records = MedicalRecord.query.filter_by(
        patient_id=patient.id
    ).order_by(MedicalRecord.visit_date.desc()).limit(3).all()
    active_prescriptions = Prescription.query.filter_by(
        patient_id=patient.id, is_active=True
    ).order_by(Prescription.prescription_date.desc()).limit(3).all()
    return render_template('patient/dashboard.html',
                           patient=patient,
                           upcoming_appointments=upcoming_appointments,
                           medical_records=medical_records,
                           active_prescriptions=active_prescriptions)


@patient_bp.route('/appointments')
@login_required
@patient_required
def appointments():
    patient = current_user.patient_profile
    appointments_list = Appointment.query.filter_by(
        patient_id=patient.id
    ).order_by(Appointment.appointment_date.desc()).all()
    return render_template('patient/appointments.html', appointments=appointments_list)


@patient_bp.route('/medical-records')
@login_required
@patient_required
def medical_records():
    patient = current_user.patient_profile
    records = MedicalRecord.query.filter_by(
        patient_id=patient.id
    ).order_by(MedicalRecord.visit_date.desc()).all()
    return render_template('patient/medical_records.html', records=records)


@patient_bp.route('/prescriptions')
@login_required
@patient_required
def prescriptions():
    patient = current_user.patient_profile
    prescriptions_list = Prescription.query.filter_by(
        patient_id=patient.id
    ).order_by(Prescription.prescription_date.desc()).all()
    return render_template('patient/prescriptions.html', prescriptions=prescriptions_list)
