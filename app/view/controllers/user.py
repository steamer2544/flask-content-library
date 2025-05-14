from flask import Blueprint, render_template


bp = Blueprint('user', __name__)

@bp.route("/", methods=["GET"])
def index():
    # posts = Post.query.order_by(Post.created_at.desc()).all()
    # return render_template('index.html', posts=posts)
    return render_template('user.html')