from config import Config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask_bootstrap import Bootstrap
from flask_moment import Moment

import logging

import os

from flask_mail import Mail

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# Only needed if using the flask_migrate/Alembic - using either flask-sqlacodegen or schema metadata instead.
# See models.py
#
# migrate = Migrate(app, db)

#  flask_login setup
login = LoginManager(app)
login.login_view = 'login'

#  flask_login user loader setup

@login.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))


mail = Mail(app)

bootstrap = Bootstrap(app)

moment = Moment(app)

if not app.debug:

    # MAIL SETUP

    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # LOGGING SETUP - To do logging just import logging in the relevant .py file.

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

# Non-circular import
from app import routes, models, errors
