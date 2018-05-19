import os

# basedir = os.path.abspath(os.path.dirname(__file__))
#
#        'sqlite:///' + os.path.join(basedir, 'app.db')
#        'oracle://peter:Oracle_1@127.0.0.1:1521/ORCLPDB'

class Config(object):

    # sqlalchemy config

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'oracle://mega:mega@ORCLPDB'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # email config

    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    # application config

    POSTS_PER_PAGE = 10
