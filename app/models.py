from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
import uuid

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    tel = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer)
    created_by = db.Column(UUID(as_uuid=True), nullable=True)
    created_at = db.Column(db.DateTime)
    updated_by = db.Column(UUID(as_uuid=True), nullable=True)
    updated_at = db.Column(db.DateTime)
    deleted_by = db.Column(UUID(as_uuid=True), nullable=True)
    deleted_at = db.Column(db.DateTime)
    roles = db.relationship(
        'Role',
        secondary='role_user',
        backref='users'
    )

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer)
    created_by = db.Column(UUID(as_uuid=True), nullable=True)
    created_at = db.Column(db.DateTime)
    updated_by = db.Column(UUID(as_uuid=True), nullable=True)
    updated_at = db.Column(db.DateTime)
    deleted_by = db.Column(UUID(as_uuid=True), nullable=True)
    deleted_at = db.Column(db.DateTime)
    slug = db.Column(db.String(255), nullable=True)

class RoleUser(db.Model):
    __tablename__ = 'role_user'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'))
    created_by = db.Column(UUID(as_uuid=True), nullable=True)
    created_at = db.Column(db.DateTime)
    updated_by = db.Column(UUID(as_uuid=True), nullable=True)
    updated_at = db.Column(db.DateTime)
    deleted_by = db.Column(UUID(as_uuid=True), nullable=True)
    deleted_at = db.Column(db.DateTime)
