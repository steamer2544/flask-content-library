from flask import Blueprint, request
from app.models.media import Media
from sqlalchemy import desc, asc

media_bp = Blueprint('media', __name__)

@media_bp.route("/", methods=["GET"])
def list_media():
    # Query params
    page_no = int(request.args.get('pageNo', 1))
    page_limit = int(request.args.get('pageLimit', 10))
    order_by = request.args.get('orderBy', 'created_at')
    order_direction = request.args.get('orderDirection', 'desc')
    keyword = request.args.get('keyword', '')

    # Base query
    query = Media.query.filter(Media.deleted_at == None)

    if keyword:
        search = f"%{keyword}%"
        query = query.filter(
            (Media.title.ilike(search)) |
            (Media.description.ilike(search)) |
            (Media.media_type.ilike(search))
        )

    # Sorting
    order_col = getattr(Media, order_by, Media.created_at)
    if order_direction.lower() == 'desc':
        query = query.order_by(desc(order_col))
    else:
        query = query.order_by(asc(order_col))

    # Pagination
    total = query.count()
    offset = (page_no - 1) * page_limit
    media = query.offset(offset).limit(page_limit).all()

    media_list = []
    for media_item in media:
        media_dict = {
            "id": media_item.id,
            "title": media_item.title,
            "description": media_item.description,
            "media_type": media_item.media_type,
            "file_url": media_item.file_url,
            "user_id": media_item.user_id,
            "approval_status": media_item.approval_status,
            "created_at": media_item.created_at.isoformat(),
            "updated_at": media_item.updated_at.isoformat()
        }
        media_list.append(media_dict)

    metadata = {
        "orderBy": order_by,
        "orderDirection": order_direction,
        "previousPage": page_no - 1 if page_no > 1 else None,
        "pageNo": page_no,
        "pageLimit": page_limit,
        "nextPage": page_no + 1 if offset + page_limit < total else None,
        "total": total,
        "from": offset + 1 if total > 0 else 0,
        "to": offset + len()(media_list) if total > 0 else 0,
    }

    return {
        "status": "success",
        "data": {
            "media": media_list,
            "metadata": metadata
        }
    }, 200