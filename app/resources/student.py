from flask_restful import Resource
from flask import request
from app.models.user import User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity

class StudentCreateResource(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        
        # Only allow admin to create students
        if current_user["role"] != "admin":
            return {"message": "Unauthorized"}, 403

        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        student_class = data.get("class")

        if User.query.filter_by(email=email).first():
            return {"message": "Email already in use"}, 400

        student = User(
            name=name,
            email=email,
            role="student",
            student_class=student_class,
            admission_status="Approved"
        )
        student.set_password(password)

        db.session.add(student)
        db.session.commit()

        return {
            "message": "Student account created",
            "student": {
                "id": student.id,
                "name": student.name,
                "email": student.email,
                "class": student.student_class
            }
        }, 201

class StudentChangePasswordResource(Resource):
    @jwt_required()
    def put(self):
        current_user = get_jwt_identity()

        # Only allow student
        if current_user["role"] != "student":
            return {"message": "Unauthorized"}, 403

        data = request.get_json()
        current_password = data.get("current_password")
        new_password = data.get("new_password")

        student = User.query.get(current_user["id"])

        if not student or not student.check_password(current_password):
            return {"message": "Current password is incorrect"}, 400

        student.set_password(new_password)
        db.session.commit()

        return {"message": "Password updated successfully"}, 200
            