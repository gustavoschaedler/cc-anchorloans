from flask import current_app
from flask_login import UserMixin
from image_library import db, login_manager

from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Integer, default=0)
    photos = db.relationship('Photo', backref='author', lazy=True)


class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    likes = db.Column(db.Integer, default=0)
    approved = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Photo('{self.user_id}', '{self.date_posted}')"


class Liked(db.Model):
    __tablename__ = 'liked'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='liked', lazy=True)

    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
    photo = db.relationship('Photo', backref='liked', lazy=True)

    def __repr__(self):
        return f"Liked('{self.user_id}', '{self.photo_id}')"
