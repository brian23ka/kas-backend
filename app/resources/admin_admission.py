from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.admission_letter import AdmissionLetter
from app.models.user import User
from app import db, bcrypt

def admin_only():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return {"message": "Admins only"}, 403

class AdminAdmissionListResource(Resource):
    @jwt_required()
    def get(self):
        if (res := admin_only()) is not None:
            return res

        letters = AdmissionLetter.query.all()
        return [
            {
                "id": l.id,
                "full_name": l.full_name,
                "email": l.email,
                "student_class": l.student_class,
                "status": l.status,
            }
            for l in letters
        ], 200

class AdminAdmissionApprovalResource(Resource):
    @jwt_required()
    def put(self, admission_id):
        if (res := admin_only()) is not None:
            return res

        letter = AdmissionLetter.query.get(admission_id)
        if not letter:
            return {"message": "Admission letter not found"}, 404

        if letter.status == "Approved":
            return {"message": "Already approved"}, 400

        # Update status
        letter.status = "Approved"

        # Check if user already exists
        if User.query.filter_by(email=letter.email).first():
            db.session.commit()
            return {"message": "User already exists and admission approved"}, 200

        # Create user with temp password
        temp_password = "student123"
        user = User(
            name=letter.full_name,
            email=letter.email,
            role="student",
            student_class=letter.student_class,
            admission_status="Approved"
        )
        user.set_password(temp_password)
        db.session.add(user)
        db.session.commit()

        return {
            "message": "Admission approved and student account created",
            "student": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "class": user.student_class,
                "temp_password": temp_password
            }
        }, 200

class AdminAdmissionRejectionResource(Resource):
    @jwt_required()
    def put(self, admission_id):
        if (res := admin_only()) is not None:
            return res

        letter = AdmissionLetter.query.get(admission_id)
        if not letter:
            return {"message": "Admission letter not found"}, 404

        if letter.status == "Rejected":
            return {"message": "Already rejected"}, 400

        letter.status = "Rejected"
        db.session.commit()
        return {"message": "Admission rejected"}, 200
