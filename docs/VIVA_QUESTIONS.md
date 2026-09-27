# Viva Questions & Answers
## Clinic Management System (ClinicMS)

**Prepared for:** University Oral Examination  
**Coverage:** Software Engineering, Flask, SQLAlchemy, Security, Testing, Database Design

---

## Software Engineering Concepts

**Q1. What is the Software Development Life Cycle (SDLC) and which model did you follow?**

> We followed the **Iterative model** — requirements were defined first in the SRS, then the system was built in functional modules (auth → admin → doctor → patient → appointments → records → prescriptions), tested incrementally, and refined. This suited our university project timeline. The phases were: Requirements → Design → Implementation → Testing → Documentation.

---

**Q2. What is the difference between functional and non-functional requirements? Give examples from your project.**

> **Functional requirements** define *what* the system does:
> - FR-019: The system shall allow booking appointments for future dates
> - FR-020: The system shall prevent double-booking
>
> **Non-functional requirements** define *how well* the system performs:
> - NFR-001: Passwords shall be hashed (security)
> - NFR-003: UI shall be responsive (usability)
> - NFR-004: Pages should load in under 2 seconds (performance)

---

**Q3. What is a Business Rule? Give 3 examples from your system.**

> A Business Rule is a specific constraint or policy that governs system behavior:
> - **BR-001:** Appointments can only be booked for future dates
> - **BR-002:** A doctor cannot have two appointments at the same date and time
> - **BR-007:** An admin cannot deactivate their own account

---

## Requirements Engineering

**Q4. What is an SRS document and what does it contain?**

> An **SRS (Software Requirements Specification)** is a complete document describing what a system should do. It contains:
> - Introduction and purpose
> - Problem statement
> - Stakeholder identification
> - User roles
> - Functional requirements (what features)
> - Non-functional requirements (performance, security, usability)
> - Business rules and constraints
> - Assumptions

---

**Q5. Who are the stakeholders in your system?**

> - **Clinic Administrator** — manages the system daily
> - **Doctors** — manage appointments and records
> - **Patients** — book appointments and view health data
> - **IT Department** — maintains and deploys the system
> - **University Evaluators** — assess the project quality

---

## UML & Use Cases

**Q6. What is a Use Case and what does it consist of?**

> A Use Case describes a specific interaction between an actor and the system to achieve a goal. It includes:
> - **ID and Name** (e.g., UC-005: Book Appointment)
> - **Actor** (who performs it)
> - **Preconditions** (what must be true before)
> - **Main Flow** (step-by-step happy path)
> - **Alternative Flows** (exception handling)
> - **Postconditions** (state after success)

---

**Q7. What is the difference between an Activity Diagram and a Sequence Diagram?**

> - **Activity Diagram** shows the *flow of control* and decision points within a process. Used to model workflows (e.g., the book appointment process with its validation steps).
> - **Sequence Diagram** shows *how objects interact over time* by passing messages. Used to model the communication between Browser, Flask, Blueprint, and Database during a request.

---

**Q8. What is a Class Diagram? List the classes in your system.**

> A Class Diagram shows the static structure of the system — classes, their attributes, methods, and relationships. Our classes are: `Role`, `User`, `Doctor`, `Patient`, `Appointment`, `MedicalRecord`, `Prescription`, `PrescriptionItem`. Relationships include One-to-One (User→Doctor), One-to-Many (Doctor→Appointment), and composition (Prescription→PrescriptionItem).

---

## Architecture

**Q9. Explain your system's architecture.**

> We use a **Three-Tier Layered Architecture**:
> 1. **Presentation Layer** — Jinja2 HTML templates + Bootstrap 5 CSS/JS. Renders UI and collects user input.
> 2. **Business Logic Layer** — Flask Blueprints handle routing, validation, access control, and data processing.
> 3. **Data Access Layer** — SQLAlchemy ORM translates Python object operations into SQL queries against SQLite.
>
> This separation makes the code maintainable, testable, and modular.

---

**Q10. What is a Flask Blueprint and why did you use them?**

> A **Flask Blueprint** is a way to organize routes into reusable modules. We used 7 blueprints: `auth`, `admin`, `doctor`, `patient`, `appointment`, `medical_record`, `prescription`. Benefits:
> - Separation of concerns
> - Each module independently testable
> - Cleaner URL prefix organization (e.g., `/admin/...`, `/doctor/...`)
> - Easier to scale or replace individual modules

---

## Database Design

**Q11. What is normalization? What normal form is your database in?**

> **Normalization** is the process of organizing a database to reduce redundancy and improve data integrity.
> - **1NF:** All values are atomic (no repeating groups). Medicine items are in `prescription_items`, not a comma list.
> - **2NF:** All non-key columns depend on the full primary key.
> - **3NF:** No transitive dependencies. Doctor name is not stored in the appointments table — it's fetched via `doctor_id → users.full_name`.
>
> Our database is in **Third Normal Form (3NF)**.

---

**Q12. What is a foreign key? Give an example from your schema.**

> A **foreign key** is a column in one table that references the primary key of another table, establishing a relationship.
> - `appointments.doctor_id` → `doctors.id` (links each appointment to its doctor)
> - `appointments.patient_id` → `patients.id` (links each appointment to its patient)
> - `prescription_items.prescription_id` → `prescriptions.id`

---

**Q13. How does your system prevent appointment double-booking?**

> Before creating an appointment, we query the database:
> ```python
> conflict = Appointment.query.filter_by(
>     doctor_id=doctor_id,
>     appointment_date=appt_date,
>     appointment_time=appt_time,
>     status='Scheduled'
> ).first()
> if conflict:
>     flash("Doctor already has an appointment at this time")
> ```
> Additionally, a database-level unique constraint on `(doctor_id, appointment_date, appointment_time)` provides a second layer of protection.

---

**Q14. What is an ORM? What are its advantages?**

> An **ORM (Object-Relational Mapper)** maps database tables to Python classes. SQLAlchemy is our ORM. Advantages:
> - **No raw SQL** — reduces risk of SQL injection
> - **Pythonic syntax** — `Doctor.query.filter_by(specialty='Cardiology').all()`
> - **Database portability** — switching from SQLite to PostgreSQL requires only changing the connection string
> - **Relationship navigation** — `appointment.doctor.user.full_name`

---

**Q15. Explain the relationship between User, Doctor, and Patient tables.**

> Both `Doctor` and `Patient` extend `User` via a **One-to-One relationship**. Every doctor/patient has exactly one user account for authentication. This avoids a wide single table with many NULLs. The `users` table handles login; `doctors` and `patients` tables store role-specific data. SQLAlchemy `backref` allows `user.doctor` and `user.patient` navigation.

---

## Security

**Q16. How are passwords stored in your system?**

> Passwords are **never stored in plain text**. We use Werkzeug's `generate_password_hash()` which applies **PBKDF2 with SHA-256** and a random salt:
> ```python
> user.password_hash = generate_password_hash(password)
> # Verification:
> check_password_hash(user.password_hash, input_password)
> ```
> Even if the database is compromised, attackers cannot recover original passwords.

---

**Q17. What is SQL Injection and how does your system prevent it?**

> **SQL Injection** is an attack where malicious SQL code is inserted into input fields to manipulate database queries (e.g., `' OR 1=1 --`). We prevent it by using **SQLAlchemy ORM** — all queries are parameterized automatically. No string concatenation is used to build SQL queries. Example:
> ```python
> # Safe - SQLAlchemy parameterizes this
> User.query.filter_by(username=username).first()
> # Dangerous (NOT used) - raw SQL string concat
> db.execute(f"SELECT * FROM users WHERE username='{username}'")
> ```

---

**Q18. What is the difference between Authentication and Authorization?**

> - **Authentication** — verifying *who you are*. In our system: checking username + password via `check_password_hash()`.
> - **Authorization** — verifying *what you are allowed to do*. In our system: checking the user's role before allowing access to routes via `@admin_required`, `@doctor_required` decorators.

---

**Q19. What is Role-Based Access Control (RBAC)?**

> **RBAC** is a security model where system access is based on the user's assigned role rather than individual permissions. Our three roles are `admin`, `doctor`, and `patient`. Each route is decorated with the appropriate role check. A patient trying to access `/admin/doctors` is rejected with a 403 or redirected to login.

---

## Testing

**Q20. What is the difference between Unit Testing and Integration Testing?**

> - **Unit Testing** tests a single function or class in isolation (e.g., testing `check_password()` returns True for correct password).
> - **Integration Testing** tests multiple components working together (e.g., testing the full login flow from POST request → DB query → session creation → redirect).
>
> We used Flask's **test client** which enables both types of testing without starting a real server.

---

**Q21. What are fixtures in pytest?**

> **Fixtures** in pytest are reusable setup functions that provide test dependencies. In our test suite:
> ```python
> @pytest.fixture(scope='session')
> def app():
>     """Create a test Flask app with in-memory SQLite."""
>     app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
>     return app
> ```
> The `scope='session'` means the fixture runs once for the entire test session, saving setup time.

---

**Q22. How did you test the appointment conflict detection?**

> We wrote a test that books an appointment, then tries to book another at the same doctor/date/time:
> ```python
> def test_conflict_detection(client):
>     # Book first appointment
>     client.post('/appointment/book', data={...date='2027-01-15', time='10:00'...})
>     # Try duplicate
>     response = client.post('/appointment/book', data={...same date/time...})
>     assert b'already has an appointment' in response.data
> ```

---

## Flask-Specific Questions

**Q23. What is the Flask Application Factory pattern?**

> The **Application Factory** is a function (`create_app()`) that creates and configures the Flask application instance. This pattern allows:
> - Different configurations for testing vs production
> - Multiple app instances (useful for testing)
> - Clean initialization of extensions
> ```python
> def create_app(config=None):
>     app = Flask(__name__)
>     app.config.from_object(Config)
>     db.init_app(app)
>     login_manager.init_app(app)
>     app.register_blueprint(auth_bp)
>     return app
> ```

---

**Q24. What is `@login_required` and how does it work?**

> `@login_required` is a decorator from Flask-Login. When applied to a route, it checks if there is an authenticated user in the session (`current_user.is_authenticated`). If not, it redirects to the login page. We add it to every protected route:
> ```python
> @doctor_bp.route('/dashboard')
> @login_required
> @doctor_required
> def dashboard():
>     ...
> ```

---

**Q25. How does Flask-Login know which user is logged in?**

> Flask-Login uses a **user loader function** registered with `@login_manager.user_loader`. This function takes the user ID from the session cookie and returns the User object:
> ```python
> @login_manager.user_loader
> def load_user(user_id):
>     return User.query.get(int(user_id))
> ```
> The `current_user` proxy then provides the loaded user throughout the request context.

---

## SQLAlchemy

**Q26. How do you define a relationship in SQLAlchemy?**

> Using `db.relationship()`:
> ```python
> class Doctor(db.Model):
>     appointments = db.relationship('Appointment', backref='doctor', lazy=True)
> ```
> `backref='doctor'` creates a reverse reference so `appointment.doctor` works automatically. `lazy=True` means related objects are loaded on access (lazy loading).

---

**Q27. What is the difference between `filter()` and `filter_by()` in SQLAlchemy?**

> - `filter_by()` — simple keyword arguments for equality checks:
>   ```python
>   User.query.filter_by(username='admin').first()
>   ```
> - `filter()` — more powerful, uses column expressions, supports `!=`, `LIKE`, `OR`, etc.:
>   ```python
>   User.query.filter(User.email.like(f'%{search}%')).all()
>   ```

---

## Project-Specific

**Q28. What are the limitations of your system?**

> 1. No email notifications for appointments
> 2. No billing or payment integration
> 3. No real-time features (no WebSocket/push notifications)
> 4. SQLite is not suitable for concurrent production use (should migrate to PostgreSQL)
> 5. No file uploads (e.g., lab results, X-ray images)
> 6. No self-registration for patients (admin creates accounts)
> 7. No audit trail / activity log

---

**Q29. What would you change if you had more time?**

> 1. **PostgreSQL** — replace SQLite for production-grade concurrency
> 2. **Email Notifications** — Flask-Mail for appointment reminders
> 3. **RESTful API** — separate backend for potential mobile app
> 4. **Reporting Dashboard** — charts with Chart.js for analytics
> 5. **Automated Migrations** — Flask-Migrate for schema changes
> 6. **Patient Self-Registration** — allow patients to register themselves
> 7. **Audit Logging** — track who changed what and when

---

**Q30. Why did you choose Flask over Django?**

> Flask is a **micro-framework** — it gives us full control over the project structure. Advantages for our use case:
> - **Lightweight** — no unnecessary components (no built-in admin, no ORM by default)
> - **Flexible** — we chose SQLAlchemy (Flask-SQLAlchemy), Flask-Login ourselves
> - **Learning curve** — easier to understand each component's role
> - **Blueprint pattern** — modular route organization without Django's apps overhead
> Django would be better for larger projects with more built-in features needed, but Flask was ideal for a university project where we wanted to understand the internals.
