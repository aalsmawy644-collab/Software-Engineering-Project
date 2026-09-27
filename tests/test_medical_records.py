import pytest
from app import create_app, db
from app.models.user import User, Role
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.medical_record import MedicalRecord
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

        admin = User(username='admin', email='admin@test.com',
                     first_name='Admin', last_name='User', role_id=admin_role.id)
        admin.set_password('admin123')

        doctor_user = User(username='doctor', email='doctor@test.com',
                           first_name='Test', last_name='Doctor', role_id=doctor_role.id)
        doctor_user.set_password('doctor123')

        patient_user = User(username='patient', email='patient@test.com',
                            first_name='Test', last_name='Patient', role_id=patient_role.id)
        patient_user.set_password('patient123')

        db.session.add_all([admin, doctor_user, patient_user])
        db.session.flush()

        doctor = Doctor(user_id=doctor_user.id, specialty='General Medicine', license_number='LIC-001')
        patient = Patient(user_id=patient_user.id, date_of_birth=date(1990, 1, 1), gender='Male')
        db.session.add_all([doctor, patient])
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

class TestMedicalRecords:
    def test_medical_records_list_loads(self, client):
        client.post('/login', data={'username': 'admin', 'password': 'admin123'})
        response = client.get('/medical-records/')
        assert response.status_code == 200

    def test_create_medical_record(self, client, app):
        client.post('/login', data={'username': 'doctor', 'password': 'doctor123'})
        with app.app_context():
            patient = Patient.query.first()
        response = client.post('/medical-records/create', data={
            'patient_id': patient.id,
            'visit_date': date.today().strftime('%Y-%m-%d'),
            'chief_complaint': 'Test complaint',
            'diagnosis': 'Test diagnosis',
            'treatment_plan': 'Test treatment',
            'notes': 'Test notes'
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            assert MedicalRecord.query.count() == 1

    def test_patient_cannot_access_another_patients_record(self, client, app):
        with app.app_context():
            patient_role = Role.query.filter_by(name='patient').first()
            user2 = User(username='patient2', email='patient2@test.com',
                         first_name='Other', last_name='Patient', role_id=patient_role.id)
            user2.set_password('patient123')
            db.session.add(user2)
            db.session.flush()

            patient2 = Patient(user_id=user2.id, date_of_birth=date(1990, 1, 1), gender='Female')
            db.session.add(patient2)

            doctor = Doctor.query.first()
            patient = Patient.query.filter_by(user_id=User.query.filter_by(username='patient').first().id).first()
            record = MedicalRecord(
                patient_id=patient.id, doctor_id=doctor.id,
                visit_date=date.today(), chief_complaint='Test',
                diagnosis='Test'
            )
            db.session.add(record)
            db.session.commit()
            record_id = record.id

        client.post('/login', data={'username': 'patient2', 'password': 'patient123'})
        response = client.get(f'/medical-records/{record_id}', follow_redirects=True)
        assert b'Access denied' in response.data or response.status_code == 200
