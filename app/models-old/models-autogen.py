# Not used - represents one possible way of managing the db model
# 
# This file is (mostly) created using flask-sqlacodegen:
#
# $ flask-sqlacodegen oracle://mega:mega@orclpdb --flask
#

from app import db


class Post(db.Model):
    __tablename__ = 'POSTS'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True)
    user_id = db.Column(db.ForeignKey('USERS.id'))

    user = db.relationship('User', primaryjoin='Post.user_id == User.id', backref='posts')


class User(db.Model):
    __tablename__ = 'USERS'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))