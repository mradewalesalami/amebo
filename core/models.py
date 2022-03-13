from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from core import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id) or None


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    joined_at = db.Column(db.DateTime, default=datetime.now())
    last_login = db.Column(db.DateTime)
    password_changed_at = db.Column(db.DateTime)
    
    avatars = db.relationship('Avatar', backref='user', lazy=True, cascade='all, delete, delete-orphan')
    posts = db.relationship('Post', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)


class Avatar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    
    def __repr__(self):
        return '<Avatar {}>'.format(self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    added_at = db.Column(db.DateTime)
    text = db.Column(db.Text, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.now())
    
    added_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    comments = db.relationship('Comment', backref='post', lazy=True)
    
    def __repr__(self):
        return '<Post {}>'.format(self.subject)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    added_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime, default=datetime.now())
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='RESTRICT'))
    added_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    
    def __repr__(self):
        return '<Comment {}>'.format(self.text)
