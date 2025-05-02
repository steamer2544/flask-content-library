from flask import Blueprint, request, jsonify
from auth import token_required
from models import User, Role, RoleUser
from app import db
from sqlalchemy import desc, asc
from uuid import UUID
from datetime import datetime, timezone
import uuid
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__)

def serialize_role(role):
    return {
        "id": str(role.id),
        "name": role.name,
        "status": role.status,
        "created_by": str(role.created_by) if role.created_by else None,
        "created_at": role.created_at.isoformat() if role.created_at else None,
        "updated_by": str(role.updated_by) if role.updated_by else None,
        "updated_at": role.updated_at.isoformat() if role.updated_at else None,
        "deleted_by": str(role.deleted_by) if role.deleted_by else None,
        "deleted_at": role.deleted_at.isoformat() if role.deleted_at else None,
        "slug": role.slug,
    }

def serialize_user(user, roles):
    return {
        "id": str(user.id),
        "code": user.code,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "tel": user.tel,
        "username": user.username,
        "status": user.status,
        "created_by": str(user.created_by) if user.created_by else None,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_by": str(user.updated_by) if user.updated_by else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        "deleted_by": str(user.deleted_by) if user.deleted_by else None,
        "deleted_at": user.deleted_at.isoformat() if user.deleted_at else None,
        "roles": [serialize_role(role) for role in roles]
    }


@user_bp.route('/users', methods=['GET'])
@token_required
def list_users(current_user):
    # Query params
    page_no = int(request.args.get('pageNo', 1))
    page_limit = int(request.args.get('pageLimit', 10))
    order_by = request.args.get('orderBy', 'created_at')
    order_direction = request.args.get('orderDirection', 'desc')
    keyword = request.args.get('keyword', '')

    # Base query
    query = User.query.filter(User.deleted_at == None)

    if keyword:
        search = f"%{keyword}%"
        query = query.filter(
            (User.username.ilike(search)) |
            (User.first_name.ilike(search)) |
            (User.last_name.ilike(search)) |
            (User.email.ilike(search))
        )

    # Sorting
    order_col = getattr(User, order_by, User.created_at)
    if order_direction.lower() == 'desc':
        query = query.order_by(desc(order_col))
    else:
        query = query.order_by(asc(order_col))

    # Pagination
    total = query.count()
    offset = (page_no - 1) * page_limit
    users = query.offset(offset).limit(page_limit).all()

    # Build user list
    user_list = []
    for user in users:
        role_ids = db.session.query(RoleUser.role_id).filter_by(user_id=user.id).all()
        role_ids = [r[0] for r in role_ids]
        roles = Role.query.filter(Role.id.in_(role_ids)).all()
        user_list.append(serialize_user(user, roles))

    # Metadata
    metadata = {
        "orderBy": order_by,
        "orderDirection": order_direction,
        "previousPage": page_no - 1 if page_no > 1 else None,
        "pageNo": page_no,
        "pageLimit": page_limit,
        "nextPage": page_no + 1 if offset + page_limit < total else None,
        "total": total,
        "from": offset + 1 if total > 0 else 0,
        "to": offset + len(users)
    }

    return jsonify({
        "status": "success",
        "data": {
            "metadata": metadata,
            "data": user_list
        }
    }), 200

@user_bp.route("/users", methods=["POST"])
@token_required
def create_user(current_user):
    data = request.get_json()

    # ตรวจสอบ field ที่จำเป็น
    required_fields = ['first_name', 'last_name', 'username', 'password', 'status', 'email', 'role_ids']
    for field in required_fields:
        if field not in data:
            return jsonify({"status": "error", "message": f"Missing field: {field}"}), 400

    # ตรวจซ้ำว่า username ซ้ำไหม
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"status": "error", "message": "Username already exists"}), 400

    new_user = User(
        id=uuid.uuid4() ,
        code=None,
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['username'],
        password=generate_password_hash(data['password']),
        status=data['status'],
        email=data['email'],
        tel=None,
        # created_by=current_user["id"],
        created_by = uuid.UUID(current_user["id"]),
        created_at=datetime.now(timezone.utc),
        updated_by=None,
        updated_at=datetime.now(timezone.utc),
        deleted_by=None,
        deleted_at=None
    )

    # ผูก roles จาก role_ids
    role_ids = data.get('role_ids', [])
    try:
        role_uuids = [uuid.UUID(rid) for rid in role_ids]
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid role ID format."}), 400
    roles = Role.query.filter(Role.id.in_(role_uuids)).all()
    new_user.roles = roles

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "status": "success",
        "data": {
            "id": new_user.id,
            "code": new_user.code,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name,
            "email": new_user.email,
            "tel": new_user.tel,
            "username": new_user.username,
            "status": new_user.status,
            "created_by": new_user.created_by,
            "created_at": new_user.created_at.isoformat(),
            "updated_by": new_user.updated_by,
            "updated_at": new_user.updated_at.isoformat(),
            "deleted_by": new_user.deleted_by,
            "deleted_at": new_user.deleted_at,
            "roles": [role.id for role in new_user.roles]
        },
        "message": "User created successfully."
    }), 200

@user_bp.route("/users/<uuid:user_id>", methods=["PUT"])
@token_required
def update_user(current_user, user_id):
    data = request.get_json()

    user = db.session.query(User).filter_by(id=user_id).first()
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    # อัปเดตข้อมูลพื้นฐาน
    user.first_name = data.get("first_name", user.first_name)
    user.last_name = data.get("last_name", user.last_name)
    user.email = data.get("email", user.email)
    user.status = data.get("status", user.status)
    user.updated_by = uuid.UUID(current_user["id"])
    user.updated_at = datetime.now(timezone.utc)

    # อัปเดต Roles
    if "role_ids" in data:
        roles = db.session.query(Role).filter(Role.id.in_([UUID(rid) for rid in data["role_ids"]])).all()
        user.roles = roles

    db.session.commit()

    # Response
    return jsonify({
        "status": "success",
        "data": {
            "user": {
                "id": str(user.id),
                "code": user.code,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "tel": user.tel,
                "username": user.username,
                "status": user.status,
                "created_by": str(user.created_by) if user.created_by else None,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_by": str(user.updated_by) if user.updated_by else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                "deleted_by": str(user.deleted_by) if user.deleted_by else None,
                "deleted_at": user.deleted_at.isoformat() if user.deleted_at else None,
                "roles": [{
                    "id": str(role.id),
                    "name": role.name,
                    "status": role.status,
                    "created_by": str(role.created_by) if role.created_by else None,
                    "created_at": role.created_at.isoformat() if role.created_at else None,
                    "updated_by": str(role.updated_by) if role.updated_by else None,
                    "updated_at": role.updated_at.isoformat() if role.updated_at else None,
                    "deleted_by": str(role.deleted_by) if role.deleted_by else None,
                    "deleted_at": role.deleted_at.isoformat() if role.deleted_at else None,
                    "slug": role.slug
                } for role in user.roles]
            }
        }
    }), 200


@user_bp.route("/users/<uuid:user_id>", methods=["DELETE"])
@token_required
def delete_user(current_user, user_id):
    user = User.query.filter_by(id=user_id, deleted_at=None).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found or already deleted."}), 404

    # Soft delete
    user.deleted_at = datetime.now(timezone.utc)
    user.deleted_by = uuid.UUID(current_user["id"])
    user.updated_at = datetime.now(timezone.utc)
    user.updated_by = uuid.UUID(current_user["id"])

    # ลบความสัมพันธ์กับ roles ใน role_user ด้วย (soft ด้วยการลบ record ไปเลย)
    RoleUser.query.filter_by(user_id=user.id).delete()

    db.session.commit()

    return jsonify({
        "status": "success",
        "data": 1,
        "message": "User deleted successfully."
    }), 200


@user_bp.route("/users/<uuid:user_id>", methods=["GET"])
@token_required
def get_user_by_id(current_user, user_id):
    user = User.query.filter_by(id=user_id, deleted_at=None).first()

    if not user:
        return jsonify({"status": "error", "message": "User not found."}), 404

    # ดึง roles
    role_ids = db.session.query(RoleUser.role_id).filter_by(user_id=user.id).all()
    role_ids = [r[0] for r in role_ids]
    roles = Role.query.filter(Role.id.in_(role_ids)).all()

    # แปลงเป็น dict
    user_data = {
        "id": str(user.id),
        "code": user.code,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "tel": user.tel or "",
        "username": user.username,
        "status": user.status,
        "created_by": str(user.created_by) if user.created_by else None,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_by": str(user.updated_by) if user.updated_by else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        "deleted_by": str(user.deleted_by) if user.deleted_by else None,
        "deleted_at": user.deleted_at.isoformat() if user.deleted_at else None,
        "roles": [
            {
                "id": str(role.id),
                "name": role.name,
                "status": role.status,
                "created_by": str(role.created_by) if role.created_by else None,
                "created_at": role.created_at.isoformat() if role.created_at else None,
                "updated_by": str(role.updated_by) if role.updated_by else None,
                "updated_at": role.updated_at.isoformat() if role.updated_at else None,
                "deleted_by": str(role.deleted_by) if role.deleted_by else None,
                "deleted_at": role.deleted_at.isoformat() if role.deleted_at else None,
                "slug": role.slug
            }
            for role in roles
        ]
    }

    return jsonify({
        "status": "success",
        "data": {
            "user": user_data
        }
    }), 200
