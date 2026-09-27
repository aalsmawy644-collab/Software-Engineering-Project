import pytest
from app import create_app, db
from app.models.user import User, Role
from app.models.patient import Patient
from datetime import date

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        admin_role = Role(name='admin', description='Admin')
        patient_role = Role(name='patient', description='Patient')
        db.session.add_all([admin_role, patient_role])
        db.session.commit()

        admin = User(username='admin', email='admin@test.com',
                     first_name='Admin', last_name='User', role_id=admin_role.id)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

class TestPatients:
    def test_patients_page_loads(self, client):
        client.post('/login', data={'username': 'admin', 'password': 'admin123'})
        response = client.get('/admin/patients')
        assert response.status_code == 200

    def test_add_patient(self, client, app):
        client.post('/login', data={'username': 'admin', 'password': 'admin123'})
        response = client.post('/admin/patients/add', data={
            'first_name': 'Test',
            'last_name': 'Patient',
            'username': 'testpatient',
            'email': 'testpatient@test.com',
            'password': 'password123',
            'date_of_birth': '1990-01-01',
            'gender': 'Male',
            'blood_type': 'O+',
            'address': '123 Test St',
            'phone': '555-0100',
            'emergency_contact': 'Emergency Contact',
            'emergency_phone': '555-0101',
            'allergies': 'None',
            'chronic_conditions': 'None',
            'insurance_number': 'INS-001'
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            assert Patient.query.count() == 1

    def test_add_patient_duplicate_username(self, client, app):
        client.post('/login', data={'username': 'admin', 'password': 'admin123'})
        # Add once
        client.post('/admin/patients/add', data={
            'first_name': 'Test', 'last_name': 'Patient',
            'username': 'dupuser', 'email': 'dup@test.com',
            'password': 'password123', 'date_of_birth': '1990-01-01',
            'gender': 'Male'
        })
        # Try to add again with same username
        response = client.post('/admin/patients/add', data={
            'first_name': 'Test2', 'last_name': 'Patient2',
            'username': 'dupuser', 'email': 'dup2@test.com',
            'password': 'password123', 'date_of_birth': '1991-01-01',
            'gender': 'Female'
        }, follow_redirects=True)
        assert b'already exists' in response.data

    def test_patient_model_age(self, app):
        with app.app_context():
            patient_role = Role.query.filter_by(name='patient').first()
            user = User(username='agetest', email='age@test.com',
                        first_name='Age', last_name='Test', role_id=patient_role.id)
            user.set_password('test')
            db.session.add(user)
            db.session.flush()

            patient = Patient(user_id=user.id, date_of_birth=date(1990, 1, 1), gender='Male')
            db.session.add(patient)
            db.session.commit()

            expected_age = date.today().year - 1990 - (
                (date.today().month, date.today().day) < (1, 1)
            )
            assert patient.age == expected_age
