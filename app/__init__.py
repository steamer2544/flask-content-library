import os
from dotenv import load_dotenv
from flask import Flask
from .models import db
from .auth import auth_bp
from .user import user_bp
from datetime import timedelta

# Load environment variables dynamically
# env_file = os.getenv('FLASK_ENV_FILE', '.env.dev')
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), f'../{env_file}'))

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 1)))

db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
