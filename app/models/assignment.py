from app import db
from datetime import datetime

class Assignment(db.Model):
    __tablename__ = 'assignments'  # Add this line to explicitly set the table name

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    student_class = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
