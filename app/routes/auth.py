from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from app import db
from app.models.user import User, Role
from app.models.patient import Patient

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard_redirect'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)

        if not username or not password:
            flash('يرجى إدخال اسم المستخدم وكلمة المرور.', 'danger')
            return render_template('auth/login.html')

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('اسم المستخدم أو كلمة المرور غير صحيحة.', 'danger')
            return render_template('auth/login.html')

        if not user.is_active:
            flash('تم تعطيل هذا الحساب. يرجى التواصل مع إدارة النظام.', 'danger')
            return render_template('auth/login.html')

        login_user(user, remember=bool(remember))
        flash(f'مرحباً بك مجدداً، {user.first_name}!', 'success')

        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('auth.dashboard_redirect'))

    return render_template('auth/login.html')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """تسجيل حساب جديد للمريض (Patient Self-Registration)."""
    if current_user.is_authenticated:
        return redirect(url_for('auth.dashboard_redirect'))

    if request.method == 'POST':
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        phone = request.form.get('phone', '').strip()
        date_of_birth = request.form.get('date_of_birth', '')
        gender = request.form.get('gender', '')
        blood_type = request.form.get('blood_type', '').strip()
        address = request.form.get('address', '').strip()
        emergency_contact = request.form.get('emergency_contact', '').strip()
        emergency_phone = request.form.get('emergency_phone', '').strip()
        allergies = request.form.get('allergies', '').strip()
        chronic_conditions = request.form.get('chronic_conditions', '').strip()

        errors = []
        if not all([first_name, last_name, username, email, password, date_of_birth, gender]):
            errors.append('يرجى ملء جميع الحقول المطلوبة المميزة بعلامة (*).')
        if password != confirm_password:
            errors.append('كلمتا المرور غير متطابقتين.')
        if len(password) < 6:
            errors.append('يجب ألا تقل كلمة المرور عن 6 أحرف.')
        if User.query.filter_by(username=username).first():
            errors.append('اسم المستخدم مسجل بالفعل، يرجى اختيار اسم آخر.')
        if User.query.filter_by(email=email).first():
            errors.append('البريد الإلكتروني مسجل بالفعل.')

        if errors:
            for err in errors:
                flash(err, 'danger')
            return render_template('auth/register.html', form_data=request.form)

        try:
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            flash('صيغة تاريخ الميلاد غير صحيحة.', 'danger')
            return render_template('auth/register.html', form_data=request.form)

        patient_role = Role.query.filter_by(name='patient').first()
        if not patient_role:
            patient_role = Role(name='patient', description='Patient')
            db.session.add(patient_role)
            db.session.commit()

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            phone=phone,
            role_id=patient_role.id
        )
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        patient = Patient(
            user_id=user.id,
            date_of_birth=dob,
            gender=gender,
            blood_type=blood_type,
            address=address,
            emergency_contact=emergency_contact,
            emergency_phone=emergency_phone,
            allergies=allergies,
            chronic_conditions=chronic_conditions
        )
        db.session.add(patient)
        db.session.commit()

        login_user(user)
        flash(f'تم إنشاء حسابك بنجاح! مرحباً بك يا {user.first_name} في عيادتنا.', 'success')
        return redirect(url_for('patient.dashboard'))

    return render_template('auth/register.html', form_data={})


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج بنجاح.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/dashboard')
@login_required
def dashboard_redirect():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    elif current_user.is_doctor():
        return redirect(url_for('doctor.dashboard'))
    elif current_user.is_patient():
        return redirect(url_for('patient.dashboard'))
    return redirect(url_for('auth.login'))
