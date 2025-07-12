from flask_restful import Resource
from flask import request
from app import db
from app.models.admission_letter import AdmissionLetter

class AdmissionLetterSubmissionResource(Resource):
    def post(self):
        data = request.get_json()

        # Check if email already applied
        if AdmissionLetter.query.filter_by(email=data.get("email")).first():
            return {"message": "You already applied. Please wait for approval."}, 400

        letter = AdmissionLetter(
            full_name=data.get("full_name"),
            email=data.get("email"),
            phone=data.get("phone"),
            guardian_name=data.get("guardian_name"),
            previous_school=data.get("previous_school"),
            student_class=data.get("student_class"),
        )

        db.session.add(letter)
        db.session.commit()

        return {"message": "Application submitted successfully"}, 201
