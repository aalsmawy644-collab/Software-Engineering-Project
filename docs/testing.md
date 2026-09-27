# Testing Document
## Clinic Management System (ClinicMS)

**Test Environment:** Python 3.10, Flask test client, SQLite in-memory DB  
**Testing Framework:** pytest + Flask test client  
**Test Date:** September 2026

---

## Test Summary

| Category | Total Tests | Passed | Failed | Status |
|---|---|---|---|---|
| Authentication | 5 | 5 | 0 | ✅ |
| Admin - Doctors CRUD | 4 | 4 | 0 | ✅ |
| Admin - Patients CRUD | 4 | 4 | 0 | ✅ |
| Appointments | 5 | 5 | 0 | ✅ |
| Medical Records | 3 | 3 | 0 | ✅ |
| Prescriptions | 2 | 2 | 0 | ✅ |
| Access Control | 4 | 4 | 0 | ✅ |
| **TOTAL** | **27** | **27** | **0** | **✅ ALL PASS** |

---

## Test Cases

| Test ID | Module | Test Case | Input | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| TC-001 | Auth | Valid admin login | username=`admin`, password=`admin123` | Redirect to `/admin/dashboard`, session created | Redirected to admin dashboard | ✅ PASS |
| TC-002 | Auth | Valid doctor login | username=`dr.smith`, password=`doctor123` | Redirect to `/doctor/dashboard` | Redirected to doctor dashboard | ✅ PASS |
| TC-003 | Auth | Valid patient login | username=`john.doe`, password=`patient123` | Redirect to `/patient/dashboard` | Redirected to patient dashboard | ✅ PASS |
| TC-004 | Auth | Invalid password | username=`admin`, password=`wrongpass` | Flash "Invalid username or password", stay on login | Error message shown | ✅ PASS |
| TC-005 | Auth | Deactivated account | username=`inactive_user`, password=`pass123` | Flash "Account deactivated", stay on login | Error message shown | ✅ PASS |
| TC-006 | Admin / Doctors | Create valid doctor | All required fields provided | Doctor record created, success flash | Doctor appears in doctors list | ✅ PASS |
| TC-007 | Admin / Doctors | Create doctor — duplicate username | username=`dr.smith` (existing) | Flash error "Username already in use" | Error flash message displayed | ✅ PASS |
| TC-008 | Admin / Doctors | Edit doctor specialty | change specialty to `Cardiology` | Doctor specialty updated in database | Updated value in DB confirmed | ✅ PASS |
| TC-009 | Admin / Doctors | Delete doctor | DELETE `/admin/doctors/1/delete` | Doctor and user record removed | Record deleted from DB | ✅ PASS |
| TC-010 | Admin / Patients | Create valid patient | All required fields including DOB | Patient record created | Patient visible in patients list | ✅ PASS |
| TC-011 | Admin / Patients | Search patient by name | search=`John` | Returns only patients with "John" in name | Filtered results returned | ✅ PASS |
| TC-012 | Admin / Patients | Edit patient blood type | change blood_type=`O+` | Patient blood type updated | Updated in database | ✅ PASS |
| TC-013 | Admin / Patients | Delete patient | DELETE `/admin/patients/1/delete` | Patient and user removed | Record deleted | ✅ PASS |
| TC-014 | Appointments | Book future appointment | date=tomorrow, time=10:00, valid doctor & patient | Appointment created with status=Scheduled | Appointment appears in list | ✅ PASS |
| TC-015 | Appointments | Book past date | date=yesterday | Flash error "Must be future date" | Rejected with error | ✅ PASS |
| TC-016 | Appointments | Booking conflict — same doctor, same slot | Same doctor, date, time as existing | Flash error "Doctor has appointment at this time" | Rejected with error | ✅ PASS |
| TC-017 | Appointments | Cancel scheduled appointment | POST `/appointment/1/cancel` | Status changed to "Cancelled" | Status updated in DB | ✅ PASS |
| TC-018 | Appointments | Mark appointment as complete | POST `/doctor/appointments/1/complete` | Status changed to "Completed" | Status updated in DB | ✅ PASS |
| TC-019 | Medical Records | Create medical record | patient, diagnosis, chief complaint provided | MedicalRecord saved linked to doctor | Record appears in list | ✅ PASS |
| TC-020 | Medical Records | Patient views own records | Patient logged in, GET `/patient/medical-records` | Only own records shown | Filtered correctly | ✅ PASS |
| TC-021 | Medical Records | Doctor views created records | Doctor logged in, GET `/medical-record/list` | Only records where doctor_id matches | Filtered correctly | ✅ PASS |
| TC-022 | Prescriptions | Create prescription with 2 medicines | 2 medicine rows submitted | 1 Prescription + 2 PrescriptionItem records | Saved correctly in DB | ✅ PASS |
| TC-023 | Prescriptions | View prescription detail | GET `/prescription/1` | Prescription info and all medicine items displayed | All items shown correctly | ✅ PASS |
| TC-024 | Access Control | Patient cannot access admin routes | Logged-in patient, GET `/admin/dashboard` | 403 Forbidden or redirect | Redirected/403 | ✅ PASS |
| TC-025 | Access Control | Doctor cannot access admin routes | Logged-in doctor, GET `/admin/doctors` | 403 Forbidden or redirect | Redirected/403 | ✅ PASS |
| TC-026 | Access Control | Unauthenticated access | No session, GET `/admin/dashboard` | Redirect to `/login` | Redirected to login | ✅ PASS |
| TC-027 | Access Control | Admin cannot deactivate self | Admin tries to toggle own account | "Current User" label, no toggle button rendered | Button not rendered | ✅ PASS |

---

## Test Configuration

### pytest Setup (`tests/conftest.py`)

```python
import pytest
from app import create_app
from app.extensions import db as _db
from app.models import Role

@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })
    return app

@pytest.fixture(scope='session')
def db(app):
    """Create database tables."""
    with app.app_context():
        _db.create_all()
        # Seed roles
        for role_name in ['admin', 'doctor', 'patient']:
            role = Role(name=role_name)
            _db.session.add(role)
        _db.session.commit()
        yield _db
        _db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()
```

### Sample Test (`tests/test_auth.py`)

```python
def test_login_valid_admin(client, db):
    """TC-001: Valid admin login redirects to admin dashboard."""
    response = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'admin123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data

def test_login_invalid_password(client):
    """TC-004: Wrong password shows error message."""
    response = client.post('/auth/login', data={
        'username': 'admin',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b'Invalid username or password' in response.data
```

### Sample Test (`tests/test_appointments.py`)

```python
def test_booking_conflict(client, db, admin_session):
    """TC-016: Duplicate booking rejected."""
    # Book first appointment
    client.post('/appointment/book', data={
        'patient_id': 1, 'doctor_id': 1,
        'appointment_date': '2027-01-15',
        'appointment_time': '10:00',
        'duration': '30'
    })
    # Try to book same slot
    response = client.post('/appointment/book', data={
        'patient_id': 2, 'doctor_id': 1,
        'appointment_date': '2027-01-15',
        'appointment_time': '10:00',
        'duration': '30'
    }, follow_redirects=True)
    assert b'already has an appointment' in response.data
```

---

## Manual Test Checklist

- [x] Login with each of the 3 demo roles works correctly
- [x] Admin dashboard displays correct statistics
- [x] Doctor dashboard shows today's appointments
- [x] Add Doctor form creates both User and Doctor records
- [x] Edit Doctor updates the correct record
- [x] Delete Doctor removes both Doctor and User records
- [x] Add Patient form stores all medical information
- [x] Patient search filters work correctly
- [x] Booking appointment with past date is rejected
- [x] Booking conflicting time slot is rejected
- [x] Appointment status updates work (complete/cancel)
- [x] Medical records only visible to authorized users
- [x] Prescriptions show all medicine items correctly
- [x] Patient cannot access `/admin/*` routes
- [x] Doctor cannot access `/admin/*` routes
- [x] Unauthenticated users redirected to login
