from datetime import datetime, timezone
from werkzeug.security import generate_password_hash
from app import app  # ต้อง import Flask app ของคุณ
from models import db, User, Role, RoleUser
import uuid

with app.app_context():
    db.drop_all()
    db.create_all()

    # 1. Create admin user
    user_id = uuid.uuid4()
    admin_user = User(
        id=user_id,
        code=None,
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

    # 2. Create role "Administrator"
    role_id = uuid.uuid4()
    admin_role = Role(
        id=role_id,
        name='Administrator',
        status=1,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    # 3. Link user with role
    role_user = RoleUser(
        id=uuid.uuid4(),
        user_id=user_id,
        role_id=role_id,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    db.session.add(admin_user)
    db.session.add(admin_role)
    db.session.add(role_user)
    db.session.commit()

    print("admin user with role Administrator seed success.")
