from .base import db
from sqlalchemy import Enum
import enum
from datetime import datetime, timezone

class ApproveStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    DOCUMENT = "document"
    OTHER = "other"

class Media(db.Model):
    __tablename__ = 'media'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    media_type = db.Column(db.String(50), nullable=False)  # เช่น 'video', 'image', 'pdf'
    file_url = db.Column(db.String, nullable=False)

    # ความสัมพันธ์กับ User
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('media', lazy=True), foreign_keys=[user_id])

    # สถานะการอนุมัติ
    approval_status = db.Column(db.String(20), default=ApproveStatus.PENDING)
    approved_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # ใครอนุมัติ (admin/mod)
    approved_at = db.Column(db.DateTime, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    deleted_by = db.Column(db.Integer, nullable=True)
    deleted_at = db.Column(db.DateTime)
