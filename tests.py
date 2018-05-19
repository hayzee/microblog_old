from config import Config

from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

def get_or_create(username, email):
    return User.query.filter(User.username==username).first() or User(username=username, email=email)

class UserModelCase(unittest.TestCase):

    u1, u2, u3, u4 = None, None, None, None

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI

        self.u1 = get_or_create(username='testuser01', email='testuser01@example.com')
        self.u2 = get_or_create(username='testuser02', email='testuser02@example.com')
        self.u3 = get_or_create(username='testuser03', email='testuser03@example.com')
        self.u4 = get_or_create(username='testuser04', email='testuser04@example.com')

        db.session.add_all([self.u1, self.u2, self.u3, self.u4])
        db.session.commit()


    def tearDown(self):
        print("teardown")
        for u in [self.u1, self.u2, self.u3, self.u4]:
            db.session.delete(u)
        db.session.commit()


    def test_password_hashing(self):

        u1, u2, u3, u4 = self.u1, self.u2, self.u3, self.u4

        u1.set_password('cat')
        self.assertFalse(u1.check_password('dog'))
        self.assertTrue(u1.check_password('cat'))


    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):

        u1, u2, u3, u4 = self.u1, self.u2, self.u3, self.u4

        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'testuser02')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'testuser01')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):

        u1, u2, u3, u4 = self.u1, self.u2, self.u3, self.u4

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from testuser1", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from testuser2", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from testuser3", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from testuser4", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # testuser1 follows testuser2
        u1.follow(u4)  # testuser1 follows testuser4
        u1.follow(u4)  # testuser1 follows testuser4
        u2.follow(u3)  # testuser2 follows testuser3
        u3.follow(u4)  # testuser3 follows testuser4
        db.session.commit()

        # check the followed posts of=  each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

if __name__ == '__main__':
    unittest.main(verbosity=2)

