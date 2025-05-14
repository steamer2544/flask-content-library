from flask import Blueprint, request, jsonify
from functools import wraps
from werkzeug.security import check_password_hash
from .models.user import db, User
import jwt
from datetime import datetime, timezone, timedelta
import os

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = os.environ['SECRET_KEY']


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"status": "error", "message": "Token is missing!"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            kwargs['current_user'] = data
        except jwt.ExpiredSignatureError:
            return jsonify({"status": "error", "message": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"status": "error", "message": "Invalid token!"}), 401

        return f(*args, **kwargs)

    return decorated


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

    # role_ids = db.session.query(RoleUser.role_id).filter_by(user_id=user.id).all()
    # role_ids = [r[0] for r in role_ids]
    # roles = Role.query.filter(Role.id.in_(role_ids)).all()

    payload = {
        'id': user.id,
        'username': user.username,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(days=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return jsonify({
        "status": "success",
        "data": {
            "user": serialize_user(user),
            "token": token
        }
    }), 200


# def serialize_role(role):
#     return {
#         "id": str(role.id),
#         "name": role.name,
#         "status": role.status,
#         "created_by": str(role.created_by) if role.created_by else None,
#         "created_at": role.created_at.isoformat() if role.created_at else None,
#         "updated_by": str(role.updated_by) if role.updated_by else None,
#         "updated_at": role.updated_at.isoformat() if role.updated_at else None,
#         "deleted_by": str(role.deleted_by) if role.deleted_by else None,
#         "deleted_at": role.deleted_at.isoformat() if role.deleted_at else None,
#         "slug": None
#     }

def serialize_user(user):
    return {
        "id": str(user.id),
        # "code": user.code,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "tel": user.tel,
        "username": user.username,
        "role": user.role.value,
        "school": user.school,
        "status": user.status,
        "created_by": str(user.created_by) if user.created_by else None,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_by": str(user.updated_by) if user.updated_by else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        "deleted_by": str(user.deleted_by) if user.deleted_by else None,
        "deleted_at": user.deleted_at.isoformat() if user.deleted_at else None,
        # "roles": [serialize_role(role) for role in roles]
    }

