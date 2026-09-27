from app import db
from datetime import datetime, time


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50), unique=True, nullable=False)
    experience_years = db.Column(db.Integer, default=0)
    consultation_fee = db.Column(db.Float, default=0.0)
    bio = db.Column(db.Text)
    is_available = db.Column(db.Boolean, default=True)
    working_start_time = db.Column(db.Time, default=time(9, 0), nullable=False)
    working_end_time = db.Column(db.Time, default=time(17, 0), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='doctor', lazy=True, cascade='all, delete-orphan')
    medical_records = db.relationship('MedicalRecord', backref='doctor', lazy=True)
    prescriptions = db.relationship('Prescription', backref='doctor', lazy=True)

    @property
    def working_hours_str(self):
        if self.working_start_time and self.working_end_time:
            return f"{self.working_start_time.strftime('%H:%M')} - {self.working_end_time.strftime('%H:%M')}"
        return "09:00 - 17:00"

    @property
    def working_hours_arabic(self):
        if self.working_start_time and self.working_end_time:
            def format_time_ar(t):
                h = t.hour
                m = f"{t.minute:02d}"
                period = "صباحاً" if h < 12 else "مساءً"
                h12 = h % 12 or 12
                return f"{h12}:{m} {period}"
            return f"من {format_time_ar(self.working_start_time)} إلى {format_time_ar(self.working_end_time)}"
        return "من 09:00 صباحاً إلى 05:00 مساءً"

    def __repr__(self):
        return f'<Doctor {self.user.full_name if self.user else self.id}>'
