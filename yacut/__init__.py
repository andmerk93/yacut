import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=os.getenv(
        'DATABASE_URI', default='sqlite:///db.sqlite3'
    ),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY=os.getenv('SECRET_KEY', default='SECRET_KEY'),
    JSON_AS_ASCII=False,
))

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import api_views, error_handlers, views
