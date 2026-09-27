# Entity Relationship Diagram (ERD)
## Clinic Management System (ClinicMS)

---

## ERD — Mermaid Diagram

```mermaid
erDiagram
    ROLES {
        int id PK
        string name
    }

    USERS {
        int id PK
        int role_id FK
        string username
        string email
        string password_hash
        string first_name
        string last_name
        string phone
        boolean is_active
        datetime created_at
    }

    DOCTORS {
        int id PK
        int user_id FK
        string specialty
        string license_number
        int experience_years
        float consultation_fee
        text bio
        boolean is_available
    }

    PATIENTS {
        int id PK
        int user_id FK
        date date_of_birth
        string gender
        string blood_type
        string address
        string emergency_contact
        string emergency_phone
        text allergies
        text chronic_conditions
        string insurance_number
    }

    APPOINTMENTS {
        int id PK
        int patient_id FK
        int doctor_id FK
        date appointment_date
        time appointment_time
        int duration_minutes
        text reason
        string status
        text notes
        datetime created_at
    }

    MEDICAL_RECORDS {
        int id PK
        int patient_id FK
        int doctor_id FK
        int appointment_id FK
        date visit_date
        text chief_complaint
        text diagnosis
        text treatment_plan
        text notes
        date follow_up_date
        datetime created_at
    }

    PRESCRIPTIONS {
        int id PK
        int patient_id FK
        int doctor_id FK
        int medical_record_id FK
        date prescription_date
        text instructions
        boolean is_active
        datetime created_at
    }

    PRESCRIPTION_ITEMS {
        int id PK
        int prescription_id FK
        string medicine_name
        string dosage
        string frequency
        string duration
        text instructions
    }

    ROLES ||--o{ USERS : "has role"
    USERS ||--o| DOCTORS : "has profile"
    USERS ||--o| PATIENTS : "has profile"
    DOCTORS ||--o{ APPOINTMENTS : "attends"
    PATIENTS ||--o{ APPOINTMENTS : "books"
    DOCTORS ||--o{ MEDICAL_RECORDS : "creates"
    PATIENTS ||--o{ MEDICAL_RECORDS : "has"
    APPOINTMENTS ||--o| MEDICAL_RECORDS : "linked to"
    DOCTORS ||--o{ PRESCRIPTIONS : "issues"
    PATIENTS ||--o{ PRESCRIPTIONS : "receives"
    MEDICAL_RECORDS ||--o{ PRESCRIPTIONS : "generates"
    PRESCRIPTIONS ||--o{ PRESCRIPTION_ITEMS : "contains"
```

---

## Relationship Descriptions

| Relationship | Type | Description |
|---|---|---|
| ROLES → USERS | One-to-Many | One role is assigned to many users |
| USERS → DOCTORS | One-to-One | Each doctor user has exactly one doctor profile |
| USERS → PATIENTS | One-to-One | Each patient user has exactly one patient profile |
| DOCTORS → APPOINTMENTS | One-to-Many | A doctor can have many appointments |
| PATIENTS → APPOINTMENTS | One-to-Many | A patient can book many appointments |
| DOCTORS → MEDICAL_RECORDS | One-to-Many | A doctor creates many medical records |
| PATIENTS → MEDICAL_RECORDS | One-to-Many | A patient has many medical records |
| APPOINTMENTS → MEDICAL_RECORDS | One-to-Zero/One | An appointment may optionally have one medical record |
| DOCTORS → PRESCRIPTIONS | One-to-Many | A doctor issues many prescriptions |
| PATIENTS → PRESCRIPTIONS | One-to-Many | A patient receives many prescriptions |
| MEDICAL_RECORDS → PRESCRIPTIONS | One-to-Many | A medical record may generate many prescriptions |
| PRESCRIPTIONS → PRESCRIPTION_ITEMS | One-to-Many | A prescription contains one or more medicine items |

---

## Key Design Choices

- The **User** table acts as an identity base; Doctor and Patient extend it via One-to-One relationships
- **Roles** are stored in a lookup table (not an enum) for flexibility
- **Appointments** have a composite uniqueness constraint on `(doctor_id, appointment_date, appointment_time)` to prevent double-booking
- **MedicalRecord.appointment_id** is nullable — records can exist independent of a booked appointment
- **Prescription.medical_record_id** is nullable — prescriptions can be issued standalone
