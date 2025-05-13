from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    tel = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer)
    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(db.DateTime)
    deleted_by = db.Column(db.Integer, nullable=True)
    deleted_at = db.Column(db.DateTime)
    roles = db.relationship(
        'Role',
        secondary='role_user',
        backref='users'
    )

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer)
    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(db.DateTime)
    deleted_by = db.Column(db.Integer, nullable=True)
    deleted_at = db.Column(db.DateTime)
    slug = db.Column(db.String(255), nullable=True)

class RoleUser(db.Model):
    __tablename__ = 'role_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime)
    updated_by = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(db.DateTime)
    deleted_by = db.Column(db.Integer, nullable=True)
    deleted_at = db.Column(db.DateTime)
