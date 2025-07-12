from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.admission_letter import AdmissionLetter
from app.models.user import User

class StudentAdmissionLetterResource(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        if identity["role"] != "student":
            return {"message": "Access denied"}, 403

        user = User.query.get(identity["id"])
        if not user:
            return {"message": "User not found"}, 404

        letter = AdmissionLetter.query.filter_by(email=user.email).first()
        if not letter:
            return {"message": "Admission letter not found"}, 404

        return {
            "id": letter.id,
            "full_name": letter.full_name,
            "email": letter.email,
            "student_class": letter.student_class,
            "status": letter.status
        }, 200
