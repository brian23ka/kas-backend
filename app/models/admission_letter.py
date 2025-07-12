from app import db
from datetime import datetime

class AdmissionLetter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(20), nullable=True)
    guardian_name = db.Column(db.String(100), nullable=True)
    previous_school = db.Column(db.String(150), nullable=True)
    student_class = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Pending, Approved, Rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
