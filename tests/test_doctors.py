import pytest
from app import create_app, db
from app.models.user import User, Role
from app.models.doctor import Doctor

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        admin_role = Role(name='admin', description='Admin')
        doctor_role = Role(name='doctor', description='Doctor')
        db.session.add_all([admin_role, doctor_role])
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

class TestDoctors:
    def test_doctors_page_loads(self, client):
        client.post('/login', data={'username': 'admin', 'password': 'admin123'})
        response = client.get('/admin/doctors')
        assert response.status_code == 200

    def test_add_doctor(self, client, app):
        client.post('/login', data={'username': 'admin', 'password': 'admin123'})
        response = client.post('/admin/doctors/add', data={
            'first_name': 'Test', 'last_name': 'Doctor',
            'username': 'testdoctor', 'email': 'testdoctor@test.com',
            'password': 'doctor123', 'phone': '555-0100',
            'specialty': 'Cardiology', 'license_number': 'LIC-TEST-001',
            'experience_years': 5, 'consultation_fee': 200.0, 'bio': 'Test bio'
        }, follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            assert Doctor.query.count() == 1
            doctor = Doctor.query.first()
            assert doctor.specialty == 'Cardiology'

    def test_duplicate_license_number(self, client, app):
        client.post('/login', data={'username': 'admin', 'password': 'admin123'})
        client.post('/admin/doctors/add', data={
            'first_name': 'Dr1', 'last_name': 'Test',
            'username': 'dr1', 'email': 'dr1@test.com',
            'password': 'test123', 'specialty': 'General Medicine',
            'license_number': 'LIC-DUP'
        })
        response = client.post('/admin/doctors/add', data={
            'first_name': 'Dr2', 'last_name': 'Test',
            'username': 'dr2', 'email': 'dr2@test.com',
            'password': 'test123', 'specialty': 'Cardiology',
            'license_number': 'LIC-DUP'
        }, follow_redirects=True)
        assert b'already exists' in response.data

    def test_delete_doctor(self, client, app):
        client.post('/login', data={'username': 'admin', 'password': 'admin123'})
        client.post('/admin/doctors/add', data={
            'first_name': 'Delete', 'last_name': 'Me',
            'username': 'deleteme', 'email': 'deleteme@test.com',
            'password': 'test123', 'specialty': 'General Medicine',
            'license_number': 'LIC-DEL'
        })
        with app.app_context():
            doctor = Doctor.query.first()
            doctor_id = doctor.id
        response = client.post(f'/admin/doctors/delete/{doctor_id}', follow_redirects=True)
        assert response.status_code == 200
        with app.app_context():
            assert Doctor.query.count() == 0
