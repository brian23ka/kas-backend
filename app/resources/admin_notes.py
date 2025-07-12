from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.note import Note
from app import db
from datetime import datetime

class AdminNotesResource(Resource):
    @jwt_required()
    def post(self):
        user = get_jwt_identity()
        if user["role"] != "admin":
            return {"message": "Unauthorized"}, 403

        data = request.get_json()
        title = data.get("title")
        content = data.get("content")
        subject = data.get("subject")
        student_class = data.get("student_class")
        due_date_str = data.get("due_date")

        try:
            due_date = datetime.fromisoformat(due_date_str) if due_date_str else None
        except ValueError:
            return {"message": "Invalid due_date format"}, 400

        note = Note(
            title=title,
            content=content,
            subject=subject,
            student_class=student_class,
            due_date=due_date
        )

        db.session.add(note)
        db.session.commit()

        return {"message": "Note posted successfully"}, 201
