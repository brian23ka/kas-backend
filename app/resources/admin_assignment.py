from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.assignment import Assignment
from app import db

def admin_only():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return {"message": "Admins only"}, 403

class AdminAssignmentResource(Resource):
    @jwt_required()
    def post(self):
        if (res := admin_only()) is not None:
            return res

        data = request.get_json()
        title = data.get("title")
        content = data.get("content")
        student_class = data.get("student_class")
        subject = data.get("subject")
        due_date = data.get("due_date")  # Expecting ISO string

        if not all([title, content, student_class, subject, due_date]):
            return {"message": "All fields are required"}, 400

        try:
            from datetime import datetime
            due_date_parsed = datetime.fromisoformat(due_date)
        except ValueError:
            return {"message": "Invalid due_date format. Use ISO 8601."}, 400

        assignment = Assignment(
            title=title,
            content=content,
            student_class=student_class,
            subject=subject,
            due_date=due_date_parsed
        )
        db.session.add(assignment)
        db.session.commit()

        return {"message": "Assignment posted successfully"}, 201
from flask_jwt_extended import get_jwt_identity
from app.models.assignment import Assignment

class StudentAssignmentResource(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        if identity["role"] != "student":
            return {"message": "Access denied"}, 403

        class_name = identity.get("class") or identity.get("student_class")

        assignments = Assignment.query.filter_by(student_class=class_name).all()

        return [
            {
                "id": a.id,
                "title": a.title,
                "content": a.content,
                "created_at": a.created_at.isoformat()
            }
            for a in assignments
        ], 200
