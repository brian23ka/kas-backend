import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///school.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret-key")
