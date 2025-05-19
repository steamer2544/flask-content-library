from flask import jsonify
from app.models.user import User
from app.models.media import Media
from sqlalchemy import desc, asc

def serialize_media(medium):
    return {
        "id": str(medium.id),
        "name": medium.name,
        "status": medium.status,
        "created_by": str(medium.created_by) if medium.created_by else None,
        "created_at": medium.created_at.isoformat() if medium.created_at else None,
        "updated_by": str(medium.updated_by) if medium.updated_by else None,
        "updated_at": medium.updated_at.isoformat() if medium.updated_at else None,
        "deleted_by": str(medium.deleted_by) if medium.deleted_by else None,
        "deleted_at": medium.deleted_at.isoformat() if medium.deleted_at else None,
        # "slug": medium.slug,
    }

def serialize_user(user, media):
    return {
        "id": str(user.id),
        # "code": user.code,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "tel": user.tel,
        "username": user.username,
        "status": user.status,
        "role": user.role.value,
        "created_by": str(user.created_by) if user.created_by else None,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_by": str(user.updated_by) if user.updated_by else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        "deleted_by": str(user.deleted_by) if user.deleted_by else None,
        "deleted_at": user.deleted_at.isoformat() if user.deleted_at else None,
        "media": [serialize_media(medium) for medium in media]
    }

def user_list(page_no, page_limit, order_by, order_direction, keyword):
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

    metadata, users = build_pagination_query(query, page_no, page_limit, order_by, order_direction)

    # Build user list
    user_list = []
    for user in users:
        media = Media.query.filter(Media.user_id==user.id).all()
        user_list.append(serialize_user(user, media))

    return jsonify({
        "status": "success",
        "data": {
            "metadata": metadata,
            "data": user_list
        }
    })

# waiting to put in utils/pagination.py
def build_pagination_query(query, page_no, page_limit, order_by, order_direction):
    # Sorting
    order_col = getattr(User, order_by, User.created_at)
    if order_direction.lower() == 'desc':
        query = query.order_by(desc(order_col))
    else:
        query = query.order_by(asc(order_col))

    # Pagination
    total = query.count()
    offset = (page_no - 1) * page_limit
    query_out = query.offset(offset).limit(page_limit).all()

    return {
        "orderBy": order_by,
        "orderDirection": order_direction,
        "previousPage": page_no - 1 if page_no > 1 else None,
        "pageNo": page_no,
        "pageLimit": page_limit,
        "nextPage": page_no + 1 if offset + page_limit < total else None,
        "total": total,
        "from": offset + 1 if total > 0 else 0,
        "to": offset + len(query_out)
    }, query_out
