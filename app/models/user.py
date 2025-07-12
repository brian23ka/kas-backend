from app import db, bcrypt

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'admin' or 'student'
    
    # Student-only fields
    student_class = db.Column(db.String(50))  # e.g. "Form 1", "Grade 6"
    admission_status = db.Column(db.String(20), default="Pending")  # or 'Approved'
    
    def set_password(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, plain_text_password):
        return bcrypt.check_password_hash(self.password, plain_text_password)
