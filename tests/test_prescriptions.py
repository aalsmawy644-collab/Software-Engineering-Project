import pytest
from app import create_app, db
from app.models.user import User, Role
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.prescription import Prescription, PrescriptionItem
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

        admin_user = User(username='admin', email='admin@test.com',
                          first_name='Admin', last_name='User', role_id=admin_role.id)
        admin_user.set_password('admin123')

        doctor_user = User(username='doctor', email='doctor@test.com',
                           first_name='Dr', last_name='Test', role_id=doctor_role.id)
        doctor_user.set_password('doctor123')

        patient_user = User(username='patient', email='patient@test.com',
                            first_name='Patient', last_name='Test', role_id=patient_role.id)
        patient_user.set_password('patient123')

        db.session.add_all([admin_user, doctor_user, patient_user])
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

class TestPrescriptions:
    def test_prescriptions_list_loads(self, client):
        client.post('/login', data={'username': 'admin', 'password': 'admin123'})
        response = client.get('/prescriptions/')
        assert response.status_code == 200

    def test_create_prescription(self, client, app):
        client.post('/login', data={'username': 'doctor', 'password': 'doctor123'})
        with app.app_context():
            patient = Patient.query.first()

        response = client.post('/prescriptions/create', data={
            'patient_id': patient.id,
            'prescription_date': date.today().strftime('%Y-%m-%d'),
            'instructions': 'Take after meals',
            'medicine_name': ['Amoxicillin', 'Paracetamol'],
            'dosage': ['500mg', '1000mg'],
            'frequency': ['3x daily', '2x daily'],
            'duration': ['7 days', '3 days'],
            'item_instructions': ['With full glass of water', 'For pain']
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            assert Prescription.query.count() == 1
            rx = Prescription.query.first()
            assert len(rx.items) == 2
            assert rx.items[0].medicine_name == 'Amoxicillin'

    def test_view_prescription_detail(self, client, app):
        with app.app_context():
            doctor = Doctor.query.first()
            patient = Patient.query.first()
            rx = Prescription(patient_id=patient.id, doctor_id=doctor.id,
                              prescription_date=date.today(), instructions='Take with food')
            db.session.add(rx)
            db.session.flush()
            item = PrescriptionItem(prescription_id=rx.id, medicine_name='Aspirin',
                                    dosage='81mg', frequency='Daily', duration='30 days')
            db.session.add(item)
            db.session.commit()
            rx_id = rx.id

        client.post('/login', data={'username': 'patient', 'password': 'patient123'})
        response = client.get(f'/prescriptions/{rx_id}')
        assert response.status_code == 200
        assert b'Aspirin' in response.data
