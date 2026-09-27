# Database Design
## Clinic Management System (ClinicMS)

---

## Overview

The database consists of **8 tables** with clearly defined relationships following the **Third Normal Form (3NF)**. The schema uses SQLite as the backing engine through SQLAlchemy ORM.

**Database File:** `instance/clinic.db`

---

## Table Index

| # | Table | Description |
|---|---|---|
| 1 | `roles` | User role definitions (admin, doctor, patient) |
| 2 | `users` | Core user accounts and authentication data |
| 3 | `doctors` | Extended doctor professional profile |
| 4 | `patients` | Extended patient medical profile |
| 5 | `appointments` | Scheduled meetings between doctors and patients |
| 6 | `medical_records` | Clinical documentation of patient visits |
| 7 | `prescriptions` | Doctor-issued prescriptions |
| 8 | `prescription_items` | Individual medicine items within a prescription |

---

## Table Definitions

### 1. `roles`

Stores the three user roles. Pre-seeded at startup.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique role identifier |
| `name` | VARCHAR(50) | NOT NULL, UNIQUE | Role name: `admin`, `doctor`, `patient` |

**Seeded Values:**

| id | name |
|---|---|
| 1 | admin |
| 2 | doctor |
| 3 | patient |

---

### 2. `users`

Core authentication and identity table. Every person in the system has a user record.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Unique user ID |
| `role_id` | INTEGER | NOT NULL, FK → `roles.id` | User's role |
| `username` | VARCHAR(80) | NOT NULL, UNIQUE | Login username |
| `email` | VARCHAR(120) | NOT NULL, UNIQUE | Email address |
| `password_hash` | VARCHAR(255) | NOT NULL | PBKDF2-SHA256 hashed password |
| `first_name` | VARCHAR(50) | NOT NULL | First name |
| `last_name` | VARCHAR(50) | NOT NULL | Last name |
| `phone` | VARCHAR(20) | NULLABLE | Contact phone number |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Account status flag |
| `created_at` | DATETIME | NOT NULL, DEFAULT NOW | Account creation timestamp |

**Relationships:**
- `role_id` → `roles.id` (Many-to-One)
- One-to-One → `doctors.user_id`
- One-to-One → `patients.user_id`

**Helper Methods (SQLAlchemy model):**
```python
@property
def full_name(self) -> str:
    return f"{self.first_name} {self.last_name}"

def is_admin(self) -> bool:
    return self.role.name == 'admin'

def is_doctor(self) -> bool:
    return self.role.name == 'doctor'

def is_patient(self) -> bool:
    return self.role.name == 'patient'

def check_password(self, password: str) -> bool:
    return check_password_hash(self.password_hash, password)
```

---

### 3. `doctors`

Professional profile for registered doctors. Extends `users` table.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Doctor profile ID |
| `user_id` | INTEGER | NOT NULL, UNIQUE, FK → `users.id` | Linked user account |
| `specialty` | VARCHAR(100) | NOT NULL | Medical specialty |
| `license_number` | VARCHAR(50) | NOT NULL, UNIQUE | Medical license number |
| `experience_years` | INTEGER | DEFAULT 0 | Years of professional experience |
| `consultation_fee` | FLOAT | DEFAULT 0.0 | Fee per consultation in USD |
| `bio` | TEXT | NULLABLE | Professional biography |
| `is_available` | BOOLEAN | DEFAULT TRUE | Availability for appointments |

**Relationships:**
- `user_id` → `users.id` (One-to-One)
- One-to-Many → `appointments.doctor_id`
- One-to-Many → `medical_records.doctor_id`
- One-to-Many → `prescriptions.doctor_id`

---

### 4. `patients`

Medical profile for registered patients. Extends `users` table.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Patient profile ID |
| `user_id` | INTEGER | NOT NULL, UNIQUE, FK → `users.id` | Linked user account |
| `date_of_birth` | DATE | NOT NULL | Patient date of birth |
| `gender` | VARCHAR(10) | NOT NULL | Male / Female / Other |
| `blood_type` | VARCHAR(5) | NULLABLE | ABO blood type (A+, B-, etc.) |
| `address` | VARCHAR(255) | NULLABLE | Residential address |
| `emergency_contact` | VARCHAR(100) | NULLABLE | Emergency contact name |
| `emergency_phone` | VARCHAR(20) | NULLABLE | Emergency contact phone |
| `allergies` | TEXT | NULLABLE | Known allergies |
| `chronic_conditions` | TEXT | NULLABLE | Chronic medical conditions |
| `insurance_number` | VARCHAR(50) | NULLABLE | Health insurance number |

**Computed Property:**
```python
@property
def age(self) -> int:
    today = date.today()
    return today.year - self.date_of_birth.year - (
        (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
    )
```

**Relationships:**
- `user_id` → `users.id` (One-to-One)
- One-to-Many → `appointments.patient_id`
- One-to-Many → `medical_records.patient_id`
- One-to-Many → `prescriptions.patient_id`

---

### 5. `appointments`

Scheduled interactions between patients and doctors.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Appointment ID |
| `patient_id` | INTEGER | NOT NULL, FK → `patients.id` | Patient attending |
| `doctor_id` | INTEGER | NOT NULL, FK → `doctors.id` | Doctor attending |
| `appointment_date` | DATE | NOT NULL | Date of appointment |
| `appointment_time` | TIME | NOT NULL | Time of appointment |
| `duration_minutes` | INTEGER | DEFAULT 30 | Appointment duration |
| `reason` | TEXT | NULLABLE | Patient's stated reason |
| `status` | VARCHAR(20) | NOT NULL, DEFAULT 'Scheduled' | Scheduled / Completed / Cancelled |
| `notes` | TEXT | NULLABLE | Doctor notes post-visit |
| `created_at` | DATETIME | DEFAULT NOW | Record creation timestamp |

**Status Values:** `Scheduled` → `Completed` or `Cancelled`

**Unique Constraint:** `(doctor_id, appointment_date, appointment_time)` — prevents double-booking.

---

### 6. `medical_records`

Clinical documentation created by doctors after patient visits.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Record ID |
| `patient_id` | INTEGER | NOT NULL, FK → `patients.id` | Patient this record belongs to |
| `doctor_id` | INTEGER | NOT NULL, FK → `doctors.id` | Doctor who created record |
| `appointment_id` | INTEGER | NULLABLE, FK → `appointments.id` | Optional linked appointment |
| `visit_date` | DATE | NOT NULL | Date of the visit |
| `chief_complaint` | TEXT | NOT NULL | Patient's main complaint |
| `diagnosis` | TEXT | NOT NULL | Clinical diagnosis |
| `treatment_plan` | TEXT | NULLABLE | Prescribed treatment plan |
| `notes` | TEXT | NULLABLE | Additional clinical notes |
| `follow_up_date` | DATE | NULLABLE | Scheduled follow-up date |
| `created_at` | DATETIME | DEFAULT NOW | Record creation timestamp |

**Relationships:**
- Many-to-One → `patients`, `doctors`, `appointments`
- One-to-Many → `prescriptions.medical_record_id`

---

### 7. `prescriptions`

A doctor's medication order for a patient.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Prescription ID |
| `patient_id` | INTEGER | NOT NULL, FK → `patients.id` | Patient receiving prescription |
| `doctor_id` | INTEGER | NOT NULL, FK → `doctors.id` | Doctor issuing prescription |
| `medical_record_id` | INTEGER | NULLABLE, FK → `medical_records.id` | Optional linked medical record |
| `prescription_date` | DATE | NOT NULL | Date prescription was written |
| `instructions` | TEXT | NULLABLE | General instructions (e.g., take with food) |
| `is_active` | BOOLEAN | DEFAULT TRUE | Whether prescription is still active |
| `created_at` | DATETIME | DEFAULT NOW | Record creation timestamp |

---

### 8. `prescription_items`

Individual medicine entries within a prescription. Implements One-to-Many with `prescriptions`.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY, AUTOINCREMENT | Item ID |
| `prescription_id` | INTEGER | NOT NULL, FK → `prescriptions.id` | Parent prescription |
| `medicine_name` | VARCHAR(200) | NOT NULL | Name of the medicine |
| `dosage` | VARCHAR(100) | NOT NULL | Dosage amount (e.g., 500mg) |
| `frequency` | VARCHAR(100) | NOT NULL | How often (e.g., 3x daily) |
| `duration` | VARCHAR(100) | NOT NULL | Duration of course (e.g., 7 days) |
| `instructions` | TEXT | NULLABLE | Specific instructions (e.g., after meals) |

---

## Table Relationships Summary

```
roles (1) ────────────── (*) users
users (1) ────────────── (1) doctors
users (1) ────────────── (1) patients
doctors (1) ─────────── (*) appointments
patients (1) ─────────── (*) appointments
doctors (1) ─────────── (*) medical_records
patients (1) ─────────── (*) medical_records
appointments (1) ─────── (0..1) medical_records
doctors (1) ─────────── (*) prescriptions
patients (1) ─────────── (*) prescriptions
medical_records (1) ──── (*) prescriptions
prescriptions (1) ─────── (*) prescription_items
```

---

## Normalization Analysis

### First Normal Form (1NF) ✅
All tables have atomic values, a primary key, and no repeating groups. Medicine items are stored in a separate `prescription_items` table rather than a comma-separated column.

### Second Normal Form (2NF) ✅
All non-key attributes depend on the entire primary key. No partial dependencies exist.

### Third Normal Form (3NF) ✅
No transitive dependencies. Doctor name is retrieved via `doctor_id → users.full_name`, not stored in appointments table.

---

## Design Decisions

| Decision | Rationale |
|---|---|
| Separate `doctors` and `patients` tables from `users` | Avoids NULL columns in a single-table approach; cleaner relationships |
| `roles` as a separate table | Allows future role additions without schema changes |
| `appointment_time` stored as TIME | Enables proper time-based queries and conflict detection |
| `is_active` on users | Soft account disabling without data loss |
| `is_active` on prescriptions | Allows tracking active vs historical prescriptions |
| `PrescriptionItem` as a child table | Supports multiple medicines per prescription (1NF compliance) |
| Nullable `appointment_id` on records | Medical records can exist without a linked appointment |
