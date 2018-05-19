from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
from sqlalchemy import text
from time import time
import jwt


# Load existing schema metadata
#
# Allows minimalistic expression of database entities:
#
# e.g.
#
# class Post(db.Model):
#    __table__ = db.Model.metadata.tables['posts']
#
# This could possibly be automatically generated with some form of utility.
#
db.Model.metadata.reflect(db.engine)


class DAOUserMixin:

    # This mixin saves polluting the database model with additional functionality.
    # Could go in a separate .py file - eg. model_mixins.py or something.

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


# Define a reference table - e.g. a many to many
# Note: These types of tables don't need classes of their own unless
# they are entities in their own right.
followers = db.Model.metadata.tables['followers']


class User(DAOUserMixin, UserMixin, db.Model):
    __table__ = db.Model.metadata.tables['users']

    followed = db.relationship(
        'User', secondary=followers,
        # primaryjoin=(followers.c.follower_id == id),
        # secondaryjoin=(followers.c.followed_id == id),
        # backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
        primaryjoin="followers.c.follower_id == User.id",
        secondaryjoin="followers.c.followed_id == User.id",
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    # The lesson here is: when using lazy='dynamic' put relationship on the 1 end of the 1:m
    posts = db.relationship('Post', primaryjoin='User.id == Post.user_id', backref='author', lazy='dynamic',
                            cascade="all, delete-orphan")

    def __repr__(self):
        return '<User {} {}>'.format(self.id, self.username)


class Post(db.Model):
    __table__ = db.Model.metadata.tables['posts']

    # lesson: can't say lazy='dynamic' here - (because only getting one value?)
    # author = db.relationship('User', primaryjoin='Post.user_id == User.id', backref='posts', lazy='dynamic')

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# Added this entity just to show that it's possible to have an entity whos primary key comes from a sequence
# most legacy (Oracle) code will be like that.
class Sausage(db.Model):
    __table__ = db.Model.metadata.tables['sausage']

    def __repr__(self):
        return '<Sausage {}>'.format(self.name)


# Arbitrary run-anything function which returns whatever db.engine.execute returns.
def run_sql(sql, binds):
    return db.engine.execute(text(sql), binds)

# Now defined in __init__ though miguel has it defined here. Not sure if that matters. It doesn't seem to.
#
# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))
