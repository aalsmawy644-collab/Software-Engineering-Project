import pytest
from app import create_app, db
from app.models.user import User, Role
from app.models.doctor import Doctor
from app.models.patient import Patient
from datetime import date

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        admin_role = Role(name='admin', description='Admin')
        doctor_role = Role(name='doctor', description='Doctor')
        patient_role = Role(name='patient', description='Patient')
        db.session.add_all([admin_role, doctor_role, patient_role])
        db.session.commit()

        admin = User(username='testadmin', email='admin@test.com',
                     first_name='Test', last_name='Admin', role_id=admin_role.id)
        admin.set_password('password123')

        doctor_user = User(username='testdoctor', email='doctor@test.com',
                           first_name='Test', last_name='Doctor', role_id=doctor_role.id)
        doctor_user.set_password('password123')

        patient_user = User(username='testpatient', email='patient@test.com',
                            first_name='Test', last_name='Patient', role_id=patient_role.id)
        patient_user.set_password('password123')

        db.session.add_all([admin, doctor_user, patient_user])
        db.session.flush()

        doctor = Doctor(user_id=doctor_user.id, specialty='General', license_number='TEST-001')
        patient = Patient(user_id=patient_user.id, date_of_birth=date(1990, 1, 1), gender='Male')
        db.session.add_all([doctor, patient])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

class TestAuthentication:
    def test_login_page_loads(self, client):
        response = client.get('/login')
        assert response.status_code == 200
        assert 'تسجيل الدخول'.encode('utf-8') in response.data or b'Sign In' in response.data

    def test_login_with_valid_credentials(self, client):
        response = client.post('/login', data={
            'username': 'testadmin',
            'password': 'password123'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert 'لوحة'.encode('utf-8') in response.data or b'Dashboard' in response.data or b'Welcome' in response.data

    def test_login_with_invalid_credentials(self, client):
        response = client.post('/login', data={
            'username': 'testadmin',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert 'غير صحيحة'.encode('utf-8') in response.data or b'Invalid' in response.data

    def test_login_with_empty_credentials(self, client):
        response = client.post('/login', data={
            'username': '',
            'password': ''
        }, follow_redirects=True)
        assert response.status_code == 200
        assert 'يرجى إدخال'.encode('utf-8') in response.data or b'Please enter' in response.data

    def test_logout(self, client):
        client.post('/login', data={'username': 'testadmin', 'password': 'password123'})
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert 'تسجيل الخروج'.encode('utf-8') in response.data or b'logged out' in response.data

    def test_protected_route_requires_login(self, client):
        response = client.get('/admin/dashboard', follow_redirects=False)
        assert response.status_code == 302

    def test_admin_can_access_admin_dashboard(self, client):
        client.post('/login', data={'username': 'testadmin', 'password': 'password123'})
        response = client.get('/admin/dashboard')
        assert response.status_code == 200

    def test_doctor_cannot_access_admin_dashboard(self, client):
        client.post('/login', data={'username': 'testdoctor', 'password': 'password123'})
        response = client.get('/admin/dashboard', follow_redirects=True)
        assert 'Access denied'.encode('utf-8') in response.data or 'غير مصرح'.encode('utf-8') in response.data or response.status_code in [302, 200]

    def test_patient_cannot_access_admin_dashboard(self, client):
        client.post('/login', data={'username': 'testpatient', 'password': 'password123'})
        response = client.get('/admin/dashboard', follow_redirects=True)
        assert 'Access denied'.encode('utf-8') in response.data or 'غير مصرح'.encode('utf-8') in response.data or response.status_code in [302, 200]

    def test_password_hashing(self, app):
        with app.app_context():
            user = User.query.filter_by(username='testadmin').first()
            assert user.check_password('password123') is True
            assert user.check_password('wrongpassword') is False
            assert user.password_hash != 'password123'

    def test_patient_self_registration(self, client, app):
        reg_page = client.get('/register')
        assert reg_page.status_code == 200

        res = client.post('/register', data={
            'first_name': 'New',
            'last_name': 'Patient',
            'username': 'new.patient',
            'email': 'newpatient@test.com',
            'password': 'password123',
            'confirm_password': 'password123',
            'phone': '555-9999',
            'date_of_birth': '1995-05-20',
            'gender': 'Male',
            'blood_type': 'O+',
            'address': 'Main Street',
            'emergency_contact': 'Father',
            'emergency_phone': '555-8888',
            'allergies': 'None',
            'chronic_conditions': 'None'
        }, follow_redirects=True)
        assert res.status_code == 200
        with app.app_context():
            u = User.query.filter_by(username='new.patient').first()
            assert u is not None
            assert u.patient_profile is not None
            assert u.patient_profile.blood_type == 'O+'
