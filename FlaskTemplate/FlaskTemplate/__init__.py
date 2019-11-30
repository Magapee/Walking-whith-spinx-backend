"""
The flask application package.
"""
from flask_sqlalchemy import SQLAlchemy 
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
loginManager = LoginManager()
loginManager.init_app(app)



import FlaskTemplate.views
