import os
from flask import Flask
from .models.base import db
from .api.auth import auth_bp
from .api.user import user_bp
from .api.media import media_bp
# frontend
from .view.controller.index import index_bp
from datetime import timedelta


app = Flask(__name__, template_folder="view/templates")

app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1)))

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/api_auth')
app.register_blueprint(user_bp, url_prefix='/api_user')
app.register_blueprint(media_bp, url_prefix='/api_media')

# frontend
app.register_blueprint(index_bp, url_prefix='/')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
