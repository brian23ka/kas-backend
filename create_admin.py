from app import create_app, db
from app.models.user import User

app = create_app()

with app.app_context():
    admin = User(name="Super Admin", email="admin@school.com", role="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
    print("Admin created.")
