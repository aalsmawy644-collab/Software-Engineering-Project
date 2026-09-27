# 🏥 Clinic Management System (ClinicMS)

A full-featured **Clinic Management System** built as a university capstone project using **Python Flask**, **SQLAlchemy**, **Bootstrap 5**, and **SQLite**. The system supports three distinct user roles: Administrator, Doctor, and Patient.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Demo Accounts](#demo-accounts)
- [Documentation](#documentation)

---

## ✨ Features

### 👤 Admin
- Dashboard with system statistics (Total Patients, Doctors, Appointments)
- Full CRUD for Doctors (Specialties, License, Experience, Fees)
- Full CRUD for Patients (Medical history, Demographics, Blood type)
- User account management (activate/deactivate access)
- System-wide appointment and medical record oversight

### 🩺 Doctor
- Personal dashboard with today's consultation schedule
- Manage appointments (view queue, complete visits)
- Create and manage Electronic Medical Records (EMRs)
- Formulate multi-item digital prescriptions with dosages and frequencies
- Edit personal profile, bio, and consultation fees

### 🧑‍⚕️ Patient
- Health dashboard with upcoming appointments and active medications
- Conflict-free appointment booking with available doctors
- View personal medical history and consultation records
- View digital prescriptions and instructions

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend Framework | Python 3.10+ / Flask 3.x |
| ORM | Flask-SQLAlchemy 3.x / SQLAlchemy 2.0 |
| Authentication | Flask-Login with Session Management |
| Password Hashing | Werkzeug Security (PBKDF2:SHA256) |
| Database | SQLite 3 |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons |
| Templating | Jinja2 |
| Automated Testing | pytest, pytest-cov |

---

## 📁 Project Structure

```
E:\phon\suftwer\
├── app\
│   ├── __init__.py           # Application factory
│   ├── models\               # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── doctor.py
│   │   ├── patient.py
│   │   ├── appointment.py
│   │   ├── medical_record.py
│   │   └── prescription.py
│   ├── routes\               # Modular blueprints
│   │   ├── auth.py
│   │   ├── admin.py
│   │   ├── doctor.py
│   │   ├── patient.py
│   │   ├── appointment.py
│   │   ├── medical_record.py
│   │   └── prescription.py
│   ├── templates\            # Jinja2 HTML templates
│   │   ├── base.html
│   │   ├── auth\
│   │   ├── admin\
│   │   ├── doctor\
│   │   ├── patient\
│   │   ├── appointments\
│   │   ├── medical_records\
│   │   └── prescriptions\
│   └── static\
│       ├── css\main.css
│       └── js\main.js
├── tests\                    # Automated test suite
│   ├── test_auth.py
│   ├── test_patients.py
│   ├── test_doctors.py
│   ├── test_appointments.py
│   ├── test_medical_records.py
│   ├── test_prescriptions.py
│   └── test_integration.py
├── docs\                     # Full software engineering documentation
│   ├── SRS.md
│   ├── use-cases.md
│   ├── architecture.md
│   ├── database-design.md
│   ├── erd.md
│   ├── testing.md
│   ├── PRESENTATION.md
│   ├── VIVA_QUESTIONS.md
│   └── diagrams\
├── config.py                 # Configuration classes
├── run.py                    # Application entry point (auto port detection)
├── seed.py                   # Database seeder with realistic test data
├── requirements.txt
├── PROJECT_REPORT.md         # 18-chapter graduation project report
├── FINAL_STATUS.md           # Final delivery and audit report
└── README.md
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```powershell
# 1. Navigate to the project directory
cd E:\phon\suftwer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Initialize the database and seed realistic demo data
python seed.py
```

---

## ▶️ Running the Application

```powershell
python run.py
```

The server will start and display the local URL (auto-selects `http://127.0.0.1:5050` or `http://localhost:5050` to avoid Windows port conflicts).

Open your browser and navigate to: **`http://localhost:5050`** (or the URL printed in your console).

---

## 👤 Demo Accounts

| Role | Username | Password | Purpose |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Full system administration, manage doctors/patients |
| **Doctor** | `dr.smith` | `doctor123` | General Medicine: Consultations, EMR, Prescriptions |
| **Doctor** | `dr.johnson` | `doctor123` | Cardiology: Specialist visits, Cardiac records |
| **Doctor** | `dr.patel` | `doctor123` | Dermatology: Skin consults |
| **Patient** | `john.doe` | `patient123` | Patient self-service, Book appointments, View Rx |
| **Patient** | `jane.doe` | `patient123` | Patient records, Cardiac follow-up |
| **Patient** | `bob.wilson` | `patient123` | Patient self-service |

---

## 🧪 Running Tests

```powershell
pytest -v
```

All 31 unit, integration, and end-to-end tests will execute and pass.

---

## 📚 Documentation Deliverables

All documentation files are located in `/docs` and the root folder:

| Document | Description |
|---|---|
| [PROJECT_REPORT.md](PROJECT_REPORT.md) | Full 18-chapter academic project report |
| [FINAL_STATUS.md](FINAL_STATUS.md) | Final status and QA audit report |
| [docs/SRS.md](docs/SRS.md) | Software Requirements Specification (FR-001–030, NFRs) |
| [docs/use-cases.md](docs/use-cases.md) | Complete Use Case Specifications (UC-001–010) |
| [docs/architecture.md](docs/architecture.md) | Layered MVC Architecture & Data Flow |
| [docs/database-design.md](docs/database-design.md) | Relational Database Schema & Data Dictionary |
| [docs/erd.md](docs/erd.md) | Entity Relationship Diagram (Mermaid) |
| [docs/testing.md](docs/testing.md) | Test Cases, Scenarios & Results |
| [docs/PRESENTATION.md](docs/PRESENTATION.md) | 15-Slide Presentation Content |
| [docs/VIVA_QUESTIONS.md](docs/VIVA_QUESTIONS.md) | 30 Viva/Oral Defense Questions & Answers |
| [docs/diagrams/](docs/diagrams/) | Mermaid Class, Activity, Sequence & Use Case Diagrams |

---

## 🔒 Security Features

- Passwords hashed with PBKDF2-SHA256 (Werkzeug Security).
- Session management via Flask-Login with HTTP-only cookies.
- Role-based access control (RBAC) on all routes.
- SQL injection prevention via SQLAlchemy ORM parameterized queries.
- XSS prevention via automatic Jinja2 contextual escaping.
