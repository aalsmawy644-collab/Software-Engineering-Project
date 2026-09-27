# Activity Diagrams
## Clinic Management System (ClinicMS)

---

## 1. Login Process Activity Diagram

```mermaid
flowchart TD
    A([Start]) --> B["User navigates to /login"]
    B --> C["User enters username & password"]
    C --> D["System queries DB for username"]
    D --> E{Username\nexists?}
    E -->|No| F["Flash: Invalid credentials"]
    F --> C
    E -->|Yes| G["check_password_hash()"]
    G --> H{Password\ncorrect?}
    H -->|No| F
    H -->|Yes| I{Account\nactive?}
    I -->|No| J["Flash: Account deactivated"]
    J --> C
    I -->|Yes| K["login_user() - create session"]
    K --> L{Check user\nrole}
    L -->|admin| M["Redirect to /admin/dashboard"]
    L -->|doctor| N["Redirect to /doctor/dashboard"]
    L -->|patient| O["Redirect to /patient/dashboard"]
    M --> P([End])
    N --> P
    O --> P
```

---

## 2. Book Appointment Activity Diagram

```mermaid
flowchart TD
    A([Start]) --> B["User navigates to /appointment/book"]
    B --> C["User selects Patient, Doctor, Date, Time, Duration"]
    C --> D["User submits form"]
    D --> E{All required\nfields provided?}
    E -->|No| F["Show validation errors"]
    F --> C
    E -->|Yes| G{Is selected\ndate in future?}
    G -->|No| H["Flash: Must be future date"]
    H --> C
    G -->|Yes| I{Doctor available\nat this time?}
    I -->|No| J["Flash: Doctor already has appointment"]
    J --> C
    I -->|Yes| K["Create Appointment record\nstatus = Scheduled"]
    K --> L["Flash: Appointment booked!"]
    L --> M["Redirect to appointments list"]
    M --> N([End])
```

---

## 3. Create Medical Record Activity Diagram

```mermaid
flowchart TD
    A([Start]) --> B["Doctor navigates to /medical-record/create"]
    B --> C["Doctor selects Patient"]
    C --> D["Doctor optionally selects related Appointment"]
    D --> E["Doctor fills in:\n- Visit Date\n- Chief Complaint\n- Diagnosis\n- Treatment Plan\n- Notes\n- Follow-up Date"]
    E --> F["Doctor submits form"]
    F --> G{Required fields\npresent?}
    G -->|No| H["Highlight missing fields"]
    H --> E
    G -->|Yes| I{User is\nDoctor or Admin?}
    I -->|No| J["403 Forbidden"]
    I -->|Yes| K["Create MedicalRecord\nlinked to doctor_id"]
    K --> L{Optional:\nCreate Prescription?}
    L -->|Yes| M["Navigate to /prescription/create"]
    L -->|No| N["Flash: Record saved!"]
    M --> N
    N --> O["Redirect to medical records list"]
    O --> P([End])
```
