# for existing schemas
# requires db.Model.metadata.reflect(db.engine)

from app import db

db.Model.metadata.reflect(db.engine)

class User(db.Model):
    __table__ = db.Model.metadata.tables['users']

    def __repr__(self):
        return '<User id:{} name:{}>'.format(self.id, self.username)

class Post(db.Model):
    __table__ = db.Model.metadata.tables['posts']

    user = db.relationship('User', primaryjoin='Post.user_id == User.id', backref='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)

