from flask_restful import Resource
from flask import request
from app.models.user import User
from app import db
from flask_jwt_extended import create_access_token
from datetime import timedelta

class AdminLoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email, role="admin").first()
        if user and user.check_password(password):
            access_token = create_access_token(
                identity={"id": user.id, "role": user.role},
                expires_delta=timedelta(hours=2)
            )
            return {
                "token": access_token,
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
            }, 200
        
        return {"message": "Invalid credentials"}, 401

class StudentLoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        student = User.query.filter_by(email=email, role="student").first()
        if student and student.check_password(password):
            token = create_access_token(
                identity={"id": student.id, "role": student.role},
                expires_delta=timedelta(hours=2)
            )
            return {
                "token": token,
                "message": "Login successful",
                "user": {
                    "id": student.id,
                    "name": student.name,
                    "email": student.email,
                    "class": student.student_class
                }
            }, 200
        
        return {"message": "Invalid credentials"}, 401