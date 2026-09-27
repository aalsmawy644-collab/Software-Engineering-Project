import pytest
from app import create_app, db
from app.models.user import User, Role
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from datetime import date, time, timedelta

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

def login_as(client, username, password):
    return client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)

class TestAppointments:
    def test_book_appointment_page_loads(self, client):
        login_as(client, 'admin', 'admin123')
        response = client.get('/appointments/book')
        assert response.status_code == 200
        assert 'حجز'.encode('utf-8') in response.data or b'Book' in response.data

    def test_book_appointment_success(self, client, app):
        login_as(client, 'admin', 'admin123')
        with app.app_context():
            doctor = Doctor.query.first()
            patient = Patient.query.first()
        tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        response = client.post('/appointments/book', data={
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'appointment_date': tomorrow,
            'appointment_time': '10:00',
            'reason': 'Test appointment',
            'duration': 30
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            assert Appointment.query.count() == 1

    def test_appointment_conflict_detection(self, client, app):
        login_as(client, 'admin', 'admin123')
        with app.app_context():
            doctor = Doctor.query.first()
            patient = Patient.query.first()
        tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        # Book first appointment
        client.post('/appointments/book', data={
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'appointment_date': tomorrow,
            'appointment_time': '10:00',
            'reason': 'First',
            'duration': 30
        })
        # Try to book same slot for same doctor
        response = client.post('/appointments/book', data={
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'appointment_date': tomorrow,
            'appointment_time': '10:00',
            'reason': 'Duplicate',
            'duration': 30
        }, follow_redirects=True)
        assert 'already booked'.encode('utf-8') in response.data or 'محجوز'.encode('utf-8') in response.data

    def test_cannot_book_past_appointment(self, client, app):
        login_as(client, 'admin', 'admin123')
        with app.app_context():
            doctor = Doctor.query.first()
            patient = Patient.query.first()
        yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        response = client.post('/appointments/book', data={
            'patient_id': patient.id,
            'doctor_id': doctor.id,
            'appointment_date': yesterday,
            'appointment_time': '10:00',
            'reason': 'Past',
            'duration': 30
        }, follow_redirects=True)
        assert 'past'.encode('utf-8') in response.data.lower() or 'سابق'.encode('utf-8') in response.data

    def test_cancel_appointment(self, client, app):
        login_as(client, 'admin', 'admin123')
        with app.app_context():
            doctor = Doctor.query.first()
            patient = Patient.query.first()
            tomorrow = date.today() + timedelta(days=1)
            appt = Appointment(patient_id=patient.id, doctor_id=doctor.id,
                               appointment_date=tomorrow, appointment_time=time(14, 0), status='Scheduled')
            db.session.add(appt)
            db.session.commit()
            appt_id = appt.id

        response = client.post(f'/appointments/{appt_id}/cancel', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            appt = db.session.get(Appointment, appt_id)
            assert appt.status == 'Cancelled'

    def test_appointment_list_loads(self, client):
        login_as(client, 'admin', 'admin123')
        response = client.get('/appointments/')
        assert response.status_code == 200

    def test_cannot_book_outside_doctor_working_hours(self, client, app):
        login_as(client, 'admin', 'admin123')
        with app.app_context():
            doctor = Doctor.query.first()
            # Set doctor hours to 09:00 - 17:00
            doctor.working_start_time = time(9, 0)
            doctor.working_end_time = time(17, 0)
            db.session.commit()
            doctor_id = doctor.id
            patient = Patient.query.first()
            patient_id = patient.id

        tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

        # Try booking at 06:00 (too early)
        response_early = client.post('/appointments/book', data={
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'appointment_date': tomorrow,
            'appointment_time': '06:00',
            'reason': 'Early booking',
            'duration': 30
        }, follow_redirects=True)
        assert 'خارج'.encode('utf-8') in response_early.data or 'working hours'.encode('utf-8') in response_early.data

        # Try booking at 22:00 (too late)
        response_late = client.post('/appointments/book', data={
            'patient_id': patient_id,
            'doctor_id': doctor_id,
            'appointment_date': tomorrow,
            'appointment_time': '22:00',
            'reason': 'Late booking',
            'duration': 30
        }, follow_redirects=True)
        assert 'خارج'.encode('utf-8') in response_late.data or 'working hours'.encode('utf-8') in response_late.data

