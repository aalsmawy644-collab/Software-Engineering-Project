# Class Diagram
## Clinic Management System (ClinicMS)

---

## UML Class Diagram

```mermaid
classDiagram
    class Role {
        +int id
        +str name
    }

    class User {
        +int id
        +int role_id
        +str username
        +str email
        +str password_hash
        +str first_name
        +str last_name
        +str phone
        +bool is_active
        +datetime created_at
        +str full_name
        +bool is_admin()
        +bool is_doctor()
        +bool is_patient()
        +bool check_password(password)
        +void set_password(password)
    }

    class Doctor {
        +int id
        +int user_id
        +str specialty
        +str license_number
        +int experience_years
        +float consultation_fee
        +str bio
        +bool is_available
    }

    class Patient {
        +int id
        +int user_id
        +date date_of_birth
        +str gender
        +str blood_type
        +str address
        +str emergency_contact
        +str emergency_phone
        +str allergies
        +str chronic_conditions
        +str insurance_number
        +int age
    }

    class Appointment {
        +int id
        +int patient_id
        +int doctor_id
        +date appointment_date
        +time appointment_time
        +int duration_minutes
        +str reason
        +str status
        +str notes
        +datetime created_at
    }

    class MedicalRecord {
        +int id
        +int patient_id
        +int doctor_id
        +int appointment_id
        +date visit_date
        +str chief_complaint
        +str diagnosis
        +str treatment_plan
        +str notes
        +date follow_up_date
        +datetime created_at
    }

    class Prescription {
        +int id
        +int patient_id
        +int doctor_id
        +int medical_record_id
        +date prescription_date
        +str instructions
        +bool is_active
        +datetime created_at
    }

    class PrescriptionItem {
        +int id
        +int prescription_id
        +str medicine_name
        +str dosage
        +str frequency
        +str duration
        +str instructions
    }

    Role "1" --> "*" User : has role
    User "1" --> "0..1" Doctor : extends
    User "1" --> "0..1" Patient : extends
    Doctor "1" --> "*" Appointment : attends
    Patient "1" --> "*" Appointment : books
    Doctor "1" --> "*" MedicalRecord : creates
    Patient "1" --> "*" MedicalRecord : has
    Appointment "1" --> "0..1" MedicalRecord : linked to
    Doctor "1" --> "*" Prescription : issues
    Patient "1" --> "*" Prescription : receives
    MedicalRecord "1" --> "*" Prescription : generates
    Prescription "1" --> "*" PrescriptionItem : contains
```

---

## Class Descriptions

| Class | Type | Description |
|---|---|---|
| `Role` | Entity | Lookup table for user roles |
| `User` | Entity | Core identity and authentication |
| `Doctor` | Entity | Doctor professional profile (extends User) |
| `Patient` | Entity | Patient medical profile (extends User) |
| `Appointment` | Entity | Scheduled doctor-patient meeting |
| `MedicalRecord` | Entity | Clinical visit documentation |
| `Prescription` | Entity | Medication order by a doctor |
| `PrescriptionItem` | Entity | Single medicine in a prescription |

---

## Flask-Login Integration

The `User` class implements `Flask-Login`'s `UserMixin`:

```python
from flask_login import UserMixin

class User(db.Model, UserMixin):
    # UserMixin provides:
    # - is_authenticated (property)
    # - is_active (already defined)
    # - is_anonymous (property)
    # - get_id() (returns str(self.id))
    ...
```
