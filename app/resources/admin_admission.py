from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.admission_letter import AdmissionLetter

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
        # Implement approval logic here
        return {"message": f"Admission {admission_id} approved"}, 200

class AdminAdmissionRejectionResource(Resource):
    @jwt_required()
    def put(self, admission_id):
        # Implement rejection logic here
        return {"message": f"Admission {admission_id} rejected"}, 200
