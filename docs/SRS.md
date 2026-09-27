# Software Requirements Specification (SRS)
## Clinic Management System (ClinicMS)

**Version:** 1.0  
**Date:** September 2026  
**Prepared By:** University Software Engineering Project Team  
**Status:** Final

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Problem Statement](#2-problem-statement)
3. [Objectives](#3-objectives)
4. [Scope](#4-scope)
5. [Stakeholders](#5-stakeholders)
6. [User Roles](#6-user-roles)
7. [Functional Requirements](#7-functional-requirements)
8. [Non-Functional Requirements](#8-non-functional-requirements)
9. [Business Rules](#9-business-rules)
10. [System Constraints](#10-system-constraints)
11. [Assumptions](#11-assumptions)

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) describes the functional and non-functional requirements for the **Clinic Management System (ClinicMS)** — a web-based application designed to digitize and streamline the core operational workflows of a small-to-medium medical clinic.

### 1.2 Document Conventions
- **SHALL** indicates a mandatory requirement.
- **SHOULD** indicates a recommended requirement.
- **MAY** indicates an optional requirement.
- **FR** = Functional Requirement
- **NFR** = Non-Functional Requirement
- **BR** = Business Rule

### 1.3 Intended Audience
- University project evaluators
- Development team
- System administrators
- End users (clinic staff, doctors, patients)

### 1.4 Definitions
| Term | Definition |
|---|---|
| Admin | Clinic administrator with full system access |
| Doctor | Medical professional registered in the system |
| Patient | Registered clinic patient |
| Appointment | A scheduled meeting between a doctor and patient |
| Medical Record | Clinical documentation of a patient visit |
| Prescription | A doctor's medication order for a patient |
| RBAC | Role-Based Access Control |
| ORM | Object-Relational Mapping |

---

## 2. Problem Statement

Small and medium-sized clinics commonly rely on paper-based or spreadsheet systems to manage patient records, doctor schedules, and appointment bookings. These manual systems suffer from:

- **Data loss** due to physical damage or human error
- **Scheduling conflicts** from double-bookings
- **Poor accessibility** — records unavailable remotely
- **Inefficient searching** through physical files
- **No centralized overview** for administration

The ClinicMS addresses these pain points by providing a secure, web-based, multi-role management system.

---

## 3. Objectives

1. Provide a centralized platform for managing clinic operations
2. Enable role-based access for administrators, doctors, and patients
3. Digitize patient medical records and prescriptions
4. Prevent appointment scheduling conflicts automatically
5. Improve data security through authentication and authorization
6. Provide real-time dashboards with clinical statistics
7. Support complete CRUD operations for all major entities

---

## 4. Scope

### 4.1 In Scope
- User authentication and role management
- Doctor profile management
- Patient registration and medical profiling
- Appointment booking, viewing, completion, and cancellation
- Medical record creation and retrieval
- Prescription creation with multi-medicine support
- Admin system dashboard with statistics
- Role-specific dashboards

### 4.2 Out of Scope
- Billing and payment processing
- Integration with external lab systems
- Mobile native applications
- Multi-clinic/multi-branch support
- Insurance claim processing
- Telemedicine/video consultation

---

## 5. Stakeholders

| Stakeholder | Role | Interest |
|---|---|---|
| Clinic Administrator | Admin user | Full system control, reporting |
| Doctors | Doctor users | Schedule management, patient records |
| Patients | Patient users | Appointment booking, record viewing |
| IT Department | System maintainers | Deployment, performance |
| University Evaluators | Assessment | Code quality, documentation |

---

## 6. User Roles

### 6.1 ADMIN
The Administrator has unrestricted access to all system features.
- Manages all user accounts (create, edit, delete, activate/deactivate)
- Manages all doctor profiles and credentials
- Manages all patient profiles and medical information
- Views all appointments across all doctors
- Views all medical records and prescriptions
- Accesses system-wide statistics dashboard

### 6.2 DOCTOR
The Doctor has access to their own data and their patients' data.
- Views personal dashboard with today's schedule
- Views and manages own appointments
- Creates medical records for their patients
- Creates prescriptions for their patients
- Views the list of their own patients
- Edits personal profile and credentials

### 6.3 PATIENT
The Patient has read-only access to their own medical data.
- Views personal health dashboard
- Books appointments with available doctors
- Cancels their own scheduled appointments
- Views own appointment history
- Views own medical records
- Views own prescriptions

---

## 7. Functional Requirements

### 7.1 Authentication Module

| ID | Requirement | Priority |
|---|---|---|
| FR-001 | The system SHALL allow users to log in with username and password | High |
| FR-002 | The system SHALL authenticate users and redirect to role-specific dashboards | High |
| FR-003 | The system SHALL allow users to log out securely | High |
| FR-004 | The system SHALL enforce that unauthenticated users cannot access protected pages | High |
| FR-005 | The system SHALL hash all passwords before storing them in the database | High |

### 7.2 User Management Module

| ID | Requirement | Priority |
|---|---|---|
| FR-006 | The admin SHALL be able to view all users with their roles and status | High |
| FR-007 | The admin SHALL be able to activate or deactivate any user account | Medium |
| FR-008 | The system SHALL prevent the admin from deactivating their own account | Medium |

### 7.3 Doctor Management Module

| ID | Requirement | Priority |
|---|---|---|
| FR-009 | The admin SHALL be able to create new doctor accounts with professional details | High |
| FR-010 | The admin SHALL be able to edit doctor information (name, specialty, fee, etc.) | High |
| FR-011 | The admin SHALL be able to delete doctor accounts | Medium |
| FR-012 | The system SHALL store doctor specialty, license number, experience, and consultation fee | High |
| FR-013 | The doctor SHALL be able to update their own profile and bio | Medium |

### 7.4 Patient Management Module

| ID | Requirement | Priority |
|---|---|---|
| FR-014 | The admin SHALL be able to create new patient accounts with medical profiles | High |
| FR-015 | The admin SHALL be able to edit patient information including medical details | High |
| FR-016 | The admin SHALL be able to delete patient accounts | Medium |
| FR-017 | The admin SHALL be able to search patients by name or email | Medium |
| FR-018 | The system SHALL store patient date of birth, gender, blood type, allergies, and emergency contacts | High |

### 7.5 Appointment Management Module

| ID | Requirement | Priority |
|---|---|---|
| FR-019 | Authorized users SHALL be able to book appointments for future dates only | High |
| FR-020 | The system SHALL detect and prevent double-booking of a doctor for the same time slot | High |
| FR-021 | Doctors and admins SHALL be able to mark appointments as completed | High |
| FR-022 | Patients and admins SHALL be able to cancel scheduled appointments | High |
| FR-023 | The system SHALL display appointment status (Scheduled, Completed, Cancelled) | High |

### 7.6 Medical Record Module

| ID | Requirement | Priority |
|---|---|---|
| FR-024 | Doctors and admins SHALL be able to create medical records with diagnosis and treatment plan | High |
| FR-025 | Medical records SHALL be linked to a patient and optionally to an appointment | High |
| FR-026 | Patients SHALL be able to view their own medical records in read-only mode | High |
| FR-027 | Medical records SHALL support follow-up date scheduling | Medium |

### 7.7 Prescription Module

| ID | Requirement | Priority |
|---|---|---|
| FR-028 | Doctors and admins SHALL be able to create prescriptions with multiple medicine items | High |
| FR-029 | Each prescription item SHALL include medicine name, dosage, frequency, and duration | High |
| FR-030 | Prescriptions SHALL be linked to patients and optionally to medical records | High |

---

## 8. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-001 | Security | Passwords SHALL be hashed using PBKDF2-SHA256 with salt |
| NFR-002 | Security | All routes SHALL enforce role-based access control |
| NFR-003 | Usability | The UI SHALL be responsive and work on screen widths ≥ 768px |
| NFR-004 | Performance | Page load time SHOULD be under 2 seconds on standard hardware |
| NFR-005 | Reliability | The system SHALL maintain data integrity through database transactions |
| NFR-006 | Maintainability | Code SHALL follow PEP 8 Python style guidelines |
| NFR-007 | Maintainability | The system SHALL use Flask Blueprints for modular route organization |
| NFR-008 | Portability | The system SHALL run on Windows, macOS, and Linux |
| NFR-009 | Scalability | The database schema SHALL support migration to PostgreSQL without logic changes |
| NFR-010 | Accessibility | Flash messages SHALL provide user feedback for all actions |

---

## 9. Business Rules

| ID | Rule |
|---|---|
| BR-001 | An appointment can only be booked for a future date (today or later) |
| BR-002 | A doctor cannot have two appointments at the same date and time |
| BR-003 | Only Scheduled appointments can be cancelled or completed |
| BR-004 | Medical records can only be created by Doctors or Admins |
| BR-005 | A patient can only view their own records, not other patients' |
| BR-006 | A doctor can only view records they created, unless admin |
| BR-007 | An admin cannot deactivate their own account |
| BR-008 | Deleting a doctor also removes their associated profile data |
| BR-009 | Each prescription must have at least one medicine item |
| BR-010 | A user's role is assigned at creation and cannot be changed by the user themselves |

---

## 10. System Constraints

- **Development Environment:** Python 3.10+, Flask 3.x, SQLite
- **Browser Support:** Modern browsers (Chrome 90+, Firefox 88+, Edge 90+)
- **No JavaScript Frameworks:** Vanilla JS and Bootstrap only (no React/Vue)
- **Single-server Deployment:** Designed for single-machine deployment
- **No Real-time Features:** No WebSocket or server-sent events

---

## 11. Assumptions

1. All users have access to a modern web browser
2. The system is deployed on a local network or localhost for the university demonstration
3. Email verification is not required (simplified for academic scope)
4. The clinic operates standard business hours (08:00–18:00)
5. One role per user (no user can be both a doctor and admin simultaneously)
6. The admin creates all doctor and patient accounts (self-registration is out of scope)
7. Data is persisted in SQLite for the prototype phase
