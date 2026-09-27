from app import db
from datetime import datetime


class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    visit_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    chief_complaint = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment_plan = db.Column(db.Text)
    notes = db.Column(db.Text)
    follow_up_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    prescriptions = db.relationship('Prescription', backref='medical_record', lazy=True)

    def __repr__(self):
        return f'<MedicalRecord {self.id} - Patient {self.patient_id}>'
