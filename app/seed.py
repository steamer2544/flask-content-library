import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Absolute import for app
from app.models import db, User, Role, RoleUser
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create admin user
    admin_user = User(
        first_name='Admin',
        last_name='Admin',
        email=None,
        tel='',
        username='admin',
        password=generate_password_hash('Asdlkj123'),  # ใช้ password นี้
        status=1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    # Create role "Administrator"
    admin_role = Role(
        name='Administrator',
        status=1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    db.session.add(admin_user)
    db.session.add(admin_role)
    db.session.commit()

    # Link user with role
    role_user = RoleUser(
        user_id=admin_user.id,
        role_id=admin_role.id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    db.session.add(role_user)
    db.session.commit()

    print("admin user with role Administrator seed success.")
