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

    return app
