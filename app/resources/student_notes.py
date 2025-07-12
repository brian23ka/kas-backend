from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.note import Note

class StudentNotesResource(Resource):
    @jwt_required()
    def get(self):
        user = get_jwt_identity()
        if user["role"] != "student":
            return {"message": "Unauthorized"}, 403

        from app.models.user import User
        student = User.query.get(user["id"])
        notes = Note.query.filter_by(student_class=student.student_class).all()

        return [
            {
                "id": note.id,
                "title": note.title,
                "content": note.content,
                "subject": note.subject,
                "student_class": note.student_class,
                "created_at": note.created_at.isoformat(),
                "due_date": note.due_date.isoformat() if note.due_date else None,
            }
            for note in notes
        ]
