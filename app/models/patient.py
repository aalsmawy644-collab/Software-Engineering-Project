from app import db
from datetime import datetime


class Patient(db.Model):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_type = db.Column(db.String(5))
    address = db.Column(db.String(200))
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    allergies = db.Column(db.Text)
    chronic_conditions = db.Column(db.Text)
    insurance_number = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='patient', lazy=True, cascade='all, delete-orphan')
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy=True)
    prescriptions = db.relationship('Prescription', backref='patient', lazy=True)

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def __repr__(self):
        return f'<Patient {self.user.full_name if self.user else self.id}>'
