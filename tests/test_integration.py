import pytest
from datetime import date, time, timedelta
from app import create_app, db
from app.models.user import User, Role
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.appointment import Appointment
from app.models.medical_record import MedicalRecord
from app.models.prescription import Prescription, PrescriptionItem

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        # Seed basic roles
        admin_role = Role(name='admin', description='Admin')
        doctor_role = Role(name='doctor', description='Doctor')
        patient_role = Role(name='patient', description='Patient')
        db.session.add_all([admin_role, doctor_role, patient_role])
        db.session.commit()

        # Create Admin
        admin = User(username='admin', email='admin@clinic.com',
                     first_name='System', last_name='Admin', role_id=admin_role.id)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

class TestFullIntegrationScenario:
    """
    Phase 17 Comprehensive End-to-End Workflow:
    Admin Login -> Add Doctor -> Add Patient -> Doctor Login ->
    Book Appointment -> Conflict Detection -> Complete Appointment ->
    Create Medical Record -> Create Prescription -> Patient Views Prescription.
    """
    def test_complete_clinic_workflow(self, client, app):
        # 1. Admin Login
        login_res = client.post('/login', data={'username': 'admin', 'password': 'admin123'}, follow_redirects=True)
        assert login_res.status_code == 200
        assert 'لوحة التحكم'.encode('utf-8') in login_res.data or b'Dashboard' in login_res.data

        # 2. Admin Adds a Doctor
        add_doc_res = client.post('/admin/doctors/add', data={
            'first_name': 'Gregory', 'last_name': 'House',
            'username': 'dr.house', 'email': 'house@clinic.com',
            'password': 'doctor123', 'phone': '555-0999',
            'specialty': 'Neurology', 'license_number': 'LIC-HOUSE-1',
            'experience_years': 20, 'consultation_fee': 300.0,
            'bio': 'Diagnostic medicine expert.'
        }, follow_redirects=True)
        assert add_doc_res.status_code == 200
        assert b'House' in add_doc_res.data

        # 3. Admin Adds a Patient
        add_pat_res = client.post('/admin/patients/add', data={
            'first_name': 'Robert', 'last_name': 'Chase',
            'username': 'r.chase', 'email': 'chase@email.com',
            'password': 'patient123', 'phone': '555-0888',
            'date_of_birth': '1988-04-12', 'gender': 'Male',
            'blood_type': 'O+', 'address': '221B Baker St',
            'emergency_contact': 'Allison Cameron', 'emergency_phone': '555-0777',
            'allergies': 'Penicillin', 'chronic_conditions': 'None',
            'insurance_number': 'INS-HC-99'
        }, follow_redirects=True)
        assert add_pat_res.status_code == 200
        assert b'Chase' in add_pat_res.data

        # Admin logs out
        client.get('/logout', follow_redirects=True)

        # 4. Patient Logs In and Books Appointment
        pat_login = client.post('/login', data={'username': 'r.chase', 'password': 'patient123'}, follow_redirects=True)
        assert pat_login.status_code == 200

        with app.app_context():
            doc = Doctor.query.first()
            pat = Patient.query.first()
            assert doc is not None
            assert pat is not None

        appt_date = (date.today() + timedelta(days=2)).strftime('%Y-%m-%d')
        book_res = client.post('/appointments/book', data={
            'patient_id': pat.id,
            'doctor_id': doc.id,
            'appointment_date': appt_date,
            'appointment_time': '11:00',
            'duration': 30,
            'reason': 'Severe headache and fatigue'
        }, follow_redirects=True)
        assert book_res.status_code == 200

        # Verify conflict prevention on same slot
        conflict_res = client.post('/appointments/book', data={
            'patient_id': pat.id,
            'doctor_id': doc.id,
            'appointment_date': appt_date,
            'appointment_time': '11:00',
            'duration': 30,
            'reason': 'Duplicate attempt'
        }, follow_redirects=True)
        assert 'already booked'.encode('utf-8') in conflict_res.data or 'محجوز'.encode('utf-8') in conflict_res.data

        client.get('/logout', follow_redirects=True)

        # 5. Doctor Logs In
        doc_login = client.post('/login', data={'username': 'dr.house', 'password': 'doctor123'}, follow_redirects=True)
        assert doc_login.status_code == 200
        assert 'لوحة'.encode('utf-8') in doc_login.data or b'Dashboard' in doc_login.data

        with app.app_context():
            appt = Appointment.query.first()
            assert appt is not None
            appt_id = appt.id

        # Doctor completes appointment
        comp_res = client.post(f'/doctor/appointments/{appt_id}/complete', follow_redirects=True)
        assert comp_res.status_code == 200

        # 6. Doctor Creates Medical Record
        rec_res = client.post('/medical-records/create', data={
            'patient_id': pat.id,
            'appointment_id': appt_id,
            'visit_date': date.today().strftime('%Y-%m-%d'),
            'chief_complaint': 'Severe episodic tension headache',
            'diagnosis': 'Migraine with aura. Neurological exam normal.',
            'treatment_plan': 'Prescribe sumatriptan and lifestyle advice.',
            'notes': 'Follow up in 2 weeks if symptoms persist.'
        }, follow_redirects=True)
        assert rec_res.status_code == 200

        with app.app_context():
            med_rec = MedicalRecord.query.first()
            assert med_rec is not None
            med_rec_id = med_rec.id

        # 7. Doctor Creates Prescription
        rx_res = client.post('/prescriptions/create', data={
            'patient_id': pat.id,
            'medical_record_id': med_rec_id,
            'prescription_date': date.today().strftime('%Y-%m-%d'),
            'instructions': 'Take with plenty of water at onset of migraine aura.',
            'medicine_name': ['Sumatriptan', 'Naproxen'],
            'dosage': ['50mg', '500mg'],
            'frequency': ['As needed', 'Twice daily'],
            'duration': ['10 days', '5 days'],
            'item_instructions': ['At symptom onset', 'With meal']
        }, follow_redirects=True)
        assert rx_res.status_code == 200

        with app.app_context():
            rx = Prescription.query.first()
            assert rx is not None
            assert len(rx.items) == 2
            rx_id = rx.id

        client.get('/logout', follow_redirects=True)

        # 8. Patient Logs In and Views Prescription
        client.post('/login', data={'username': 'r.chase', 'password': 'patient123'}, follow_redirects=True)
        view_rx_res = client.get(f'/prescriptions/{rx_id}')
        assert view_rx_res.status_code == 200
        assert b'Sumatriptan' in view_rx_res.data
        assert b'Naproxen' in view_rx_res.data
        assert b'Gregory House' in view_rx_res.data
