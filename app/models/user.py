from .base import db
from sqlalchemy import Enum
import enum
from datetime import datetime, timezone


class UserRole(enum.Enum):
    ADMIN = "admin"
    MOD = "mod"
    USER = "user"

class School(enum.Enum):
    SCHOOL_A = "School A"
    SCHOOL_B = "School B"
    SCHOOL_C = "School C"
    SCHOOL_D = "School D"
    SCHOOL_E = "School E"
    SCHOOL_F = "School F"
    SCHOOL_G = "School G"
    SCHOOL_H = "School H"
    SCHOOL_I = "School I"
    SCHOOL_J = "School J"

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # code = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    school = db.Column(Enum(School), nullable=True)
    tel = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(Enum(UserRole), nullable=False, default=UserRole.USER)
    status = db.Column(db.Integer, default=1)  # 1 = active, 0 = inactive
    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_by = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    deleted_by = db.Column(db.Integer, nullable=True)
    deleted_at = db.Column(db.DateTime)
