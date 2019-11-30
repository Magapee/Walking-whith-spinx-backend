"""
The flask application package.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import DevelopmentConfig, BaseConfig


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
main_db = SQLAlchemy(app)
migrate = Migrate(app, main_db)

from FlaskTemplate import views
from FlaskTemplate import models