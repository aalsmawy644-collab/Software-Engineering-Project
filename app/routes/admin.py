from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from functools import wraps
from app import db
from app.models.user import User, Role
from app.models.doctor import Doctor
from app.models.patient import Patient
try:
    from app.models.appointment import Appointment
except ImportError:
    Appointment = None
from datetime import date, datetime, time

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('غير مصرح لك بالدخول. هذه الصفحة مخصصة لمدير النظام فقط. Access denied.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_patients = Patient.query.count()
    total_doctors = Doctor.query.count()
    total_users = User.query.count()
    today = date.today()
    if Appointment:
        todays_appointments = Appointment.query.filter_by(appointment_date=today).count()
        completed_appointments = Appointment.query.filter_by(status='Completed').count()
        scheduled_appointments = Appointment.query.filter_by(status='Scheduled').count()
        recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    else:
        todays_appointments = 0
        completed_appointments = 0
        scheduled_appointments = 0
        recent_appointments = []
    return render_template('admin/dashboard.html',
                           total_patients=total_patients,
                           total_doctors=total_doctors,
                           total_users=total_users,
                           todays_appointments=todays_appointments,
                           completed_appointments=completed_appointments,
                           scheduled_appointments=scheduled_appointments,
                           recent_appointments=recent_appointments)


@admin_bp.route('/doctors')
@login_required
@admin_required
def doctors():
    doctors_list = Doctor.query.join(User).all()
    return render_template('admin/doctors.html', doctors=doctors_list)


@admin_bp.route('/doctors/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_doctor():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        phone = request.form.get('phone', '').strip()
        specialty = request.form.get('specialty', '').strip()
        license_number = request.form.get('license_number', '').strip()
        experience_years = request.form.get('experience_years', 0)
        consultation_fee = request.form.get('consultation_fee', 0.0)
        bio = request.form.get('bio', '').strip()

        errors = []
        if not all([first_name, last_name, username, email, password, specialty, license_number]):
            errors.append('يرجى ملء جميع الحقول الإلزامية المطلوبة.')
        if User.query.filter_by(username=username).first():
            errors.append('اسم المستخدم مسجل بالفعل. Username already exists.')
        if User.query.filter_by(email=email).first():
            errors.append('البريد الإلكتروني مسجل بالفعل. Email already exists.')
        if Doctor.query.filter_by(license_number=license_number).first():
            errors.append('رقم ترخيص مزاولة المهنة مسجل بالفعل لطبيب آخر. License number already exists.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('admin/add_doctor.html')

        doctor_role = Role.query.filter_by(name='doctor').first()
        user = User(first_name=first_name, last_name=last_name,
                    username=username, email=email, phone=phone,
                    role_id=doctor_role.id)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        start_time_str = request.form.get('working_start_time', '09:00')
        end_time_str = request.form.get('working_end_time', '17:00')
        try:
            start_time_obj = datetime.strptime(start_time_str, '%H:%M').time()
        except ValueError:
            start_time_obj = time(9, 0)
        try:
            end_time_obj = datetime.strptime(end_time_str, '%H:%M').time()
        except ValueError:
            end_time_obj = time(17, 0)

        doctor = Doctor(
            user_id=user.id,
            specialty=specialty,
            license_number=license_number,
            experience_years=int(experience_years) if experience_years else 0,
            consultation_fee=float(consultation_fee) if consultation_fee else 0.0,
            bio=bio,
            working_start_time=start_time_obj,
            working_end_time=end_time_obj
        )
        db.session.add(doctor)
        db.session.commit()
        flash(f'تمت إضافة الطبيب د. {user.full_name} بنجاح إلى الكادر الطبي!', 'success')
        return redirect(url_for('admin.doctors'))

    return render_template('admin/add_doctor.html')


@admin_bp.route('/doctors/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_doctor(doctor_id):
    doctor = db.session.get(Doctor, doctor_id) or Doctor.query.get_or_404(doctor_id)
    user = doctor.user
    if request.method == 'POST':
        user.first_name = request.form.get('first_name', user.first_name).strip()
        user.last_name = request.form.get('last_name', user.last_name).strip()
        user.email = request.form.get('email', user.email).strip()
        user.phone = request.form.get('phone', user.phone or '').strip()
        doctor.specialty = request.form.get('specialty', doctor.specialty).strip()
        doctor.experience_years = int(request.form.get('experience_years', doctor.experience_years))
        doctor.consultation_fee = float(request.form.get('consultation_fee', doctor.consultation_fee))
        doctor.bio = request.form.get('bio', doctor.bio or '').strip()
        doctor.is_available = 'is_available' in request.form

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

        new_password = request.form.get('new_password', '')
        if new_password:
            user.set_password(new_password)
        db.session.commit()
        flash('تم تحديث بيانات الطبيب وساعات العمل بنجاح!', 'success')
        return redirect(url_for('admin.doctors'))
    return render_template('admin/edit_doctor.html', doctor=doctor)


@admin_bp.route('/doctors/delete/<int:doctor_id>', methods=['POST'])
@login_required
@admin_required
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    user = doctor.user
    db.session.delete(user)
    db.session.commit()
    flash('تم حذف سجل الطبيب بنجاح.', 'success')
    return redirect(url_for('admin.doctors'))


@admin_bp.route('/patients')
@login_required
@admin_required
def patients():
    search = request.args.get('search', '').strip()
    query = Patient.query.join(User)
    if search:
        query = query.filter(
            db.or_(
                User.first_name.ilike(f'%{search}%'),
                User.last_name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )
    patients_list = query.all()
    return render_template('admin/patients.html', patients=patients_list, search=search)


@admin_bp.route('/patients/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_patient():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        phone = request.form.get('phone', '').strip()
        date_of_birth = request.form.get('date_of_birth', '')
        gender = request.form.get('gender', '')
        blood_type = request.form.get('blood_type', '').strip()
        address = request.form.get('address', '').strip()
        emergency_contact = request.form.get('emergency_contact', '').strip()
        emergency_phone = request.form.get('emergency_phone', '').strip()
        allergies = request.form.get('allergies', '').strip()
        chronic_conditions = request.form.get('chronic_conditions', '').strip()
        insurance_number = request.form.get('insurance_number', '').strip()

        errors = []
        if not all([first_name, last_name, username, email, password, date_of_birth, gender]):
            errors.append('يرجى ملء جميع الحقول المطلوبة.')
        if User.query.filter_by(username=username).first():
            errors.append('اسم المستخدم مسجل بالفعل. Username already exists.')
        if User.query.filter_by(email=email).first():
            errors.append('البريد الإلكتروني مسجل بالفعل. Email already exists.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('admin/add_patient.html')

        patient_role = Role.query.filter_by(name='patient').first()
        user = User(first_name=first_name, last_name=last_name,
                    username=username, email=email, phone=phone,
                    role_id=patient_role.id)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        patient = Patient(
            user_id=user.id,
            date_of_birth=dob,
            gender=gender,
            blood_type=blood_type,
            address=address,
            emergency_contact=emergency_contact,
            emergency_phone=emergency_phone,
            allergies=allergies,
            chronic_conditions=chronic_conditions,
            insurance_number=insurance_number
        )
        db.session.add(patient)
        db.session.commit()
        flash(f'تمت إضافة المريض {user.full_name} وفتح الملف بنجاح!', 'success')
        return redirect(url_for('admin.patients'))

    return render_template('admin/add_patient.html')


@admin_bp.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    user = patient.user
    if request.method == 'POST':
        user.first_name = request.form.get('first_name', user.first_name).strip()
        user.last_name = request.form.get('last_name', user.last_name).strip()
        user.email = request.form.get('email', user.email).strip()
        user.phone = request.form.get('phone', '').strip()
        dob_str = request.form.get('date_of_birth', '')
        if dob_str:
            patient.date_of_birth = datetime.strptime(dob_str, '%Y-%m-%d').date()
        patient.gender = request.form.get('gender', patient.gender)
        patient.blood_type = request.form.get('blood_type', patient.blood_type or '').strip()
        patient.address = request.form.get('address', patient.address or '').strip()
        patient.emergency_contact = request.form.get('emergency_contact', patient.emergency_contact or '').strip()
        patient.emergency_phone = request.form.get('emergency_phone', patient.emergency_phone or '').strip()
        patient.allergies = request.form.get('allergies', patient.allergies or '').strip()
        patient.chronic_conditions = request.form.get('chronic_conditions', patient.chronic_conditions or '').strip()
        new_password = request.form.get('new_password', '')
        if new_password:
            user.set_password(new_password)
        db.session.commit()
        flash('تم تحديث بيانات المريض بنجاح!', 'success')
        return redirect(url_for('admin.patients'))
    return render_template('admin/edit_patient.html', patient=patient)


@admin_bp.route('/patients/delete/<int:patient_id>', methods=['POST'])
@login_required
@admin_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    user = patient.user
    db.session.delete(user)
    db.session.commit()
    flash('تم حذف ملف المريض بنجاح.', 'success')
    return redirect(url_for('admin.patients'))


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    users_list = User.query.all()
    return render_template('admin/users.html', users=users_list)


@admin_bp.route('/users/toggle/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('لا يمكنك تعطيل حسابك الشخصي النشط.', 'warning')
        return redirect(url_for('admin.users'))
    user.is_active = not user.is_active
    db.session.commit()
    status = 'تفعيل' if user.is_active else 'تعطيل'
    flash(f'تم {status} حساب المستخدم {user.full_name} بنجاح.', 'success')
    return redirect(url_for('admin.users'))
