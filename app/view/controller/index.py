from flask import Blueprint, render_template


index_bp = Blueprint('index', __name__)

@index_bp.route("/", methods=["GET"])
def index():
    # posts = Post.query.order_by(Post.created_at.desc()).all()
    # return render_template('index.html', posts=posts)
    return render_template('index.html')