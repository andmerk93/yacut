from os import getenv
from string import ascii_letters, digits

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

APPROVED_SYMBOLS = ascii_letters + digits
ORIGINAL_LINK_LENGTH = 256
RANDOM_GEN_TRYS = 3
SHORT_LINK_LENGTH = 16
SHORT_LINK_RANDOM_LENGTH = 6
SHORT_LINK_REXEXP = r'[A-Za-z0-9]+'

app = Flask(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY=getenv('SECRET_KEY', default='SECRET_KEY'),
    JSON_AS_ASCII=False,
))

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)

from . import api_views, error_handlers, views
