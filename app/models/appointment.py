from app import db
from datetime import datetime


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, default=30)
    status = db.Column(db.String(20), default='Scheduled', nullable=False)
    reason = db.Column(db.Text)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    STATUS_SCHEDULED = 'Scheduled'
    STATUS_COMPLETED = 'Completed'
    STATUS_CANCELLED = 'Cancelled'

    medical_record = db.relationship('MedicalRecord', backref='appointment', uselist=False)

    @property
    def datetime_str(self):
        return f"{self.appointment_date.strftime('%Y-%m-%d')} {self.appointment_time.strftime('%H:%M')}"

    def __repr__(self):
        return f'<Appointment {self.id} - {self.status}>'
