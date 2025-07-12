from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os



db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    CORS(app)
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    api = Api(app)

    # Import and register resources here
    from app.resources.auth import AdminLoginResource
    api.add_resource(AdminLoginResource, "/api/auth/admin/login")
    from app.resources.student import StudentCreateResource
    api.add_resource(StudentCreateResource, "/api/admin/students")
    from app.resources.auth import StudentLoginResource
    api.add_resource(StudentLoginResource, "/api/auth/student/login")
    from app.resources.student import StudentChangePasswordResource
    api.add_resource(StudentChangePasswordResource, "/api/student/change-password")
    from app.resources.admission import AdmissionLetterSubmissionResource
    api.add_resource(AdmissionLetterSubmissionResource, "/api/admission/apply")
    from app.resources.admin_admission import (
    AdminAdmissionListResource,
    AdminAdmissionApprovalResource,
    AdminAdmissionRejectionResource
)

    api.add_resource(AdminAdmissionListResource, "/api/admin/admissions")
    api.add_resource(AdminAdmissionApprovalResource, "/api/admin/admissions/<int:admission_id>/approve")
    api.add_resource(AdminAdmissionRejectionResource, "/api/admin/admissions/<int:admission_id>/reject")
    from app.resources.student_admission import StudentAdmissionLetterResource
    api.add_resource(StudentAdmissionLetterResource, "/api/student/admission-letter")
    from app.resources.admin_assignment import AdminAssignmentResource, StudentAssignmentResource

    api.add_resource(AdminAssignmentResource, "/api/admin/assignments")
    api.add_resource(StudentAssignmentResource, "/api/student/assignments")
    from app.resources.admin_notes import AdminNotesResource
    from app.resources.student_notes import StudentNotesResource

    api.add_resource(AdminNotesResource, "/api/admin/notes")
    api.add_resource(StudentNotesResource, "/api/student/notes")


    return app
