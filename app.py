from flask import Flask
from models import db
from auth import auth
from user import user_bp
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret-key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

db.init_app(app)

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(user_bp, url_prefix='/user')


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
