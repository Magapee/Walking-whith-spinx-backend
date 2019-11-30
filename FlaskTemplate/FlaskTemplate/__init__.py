"""
The flask application package.
"""
from flask_sqlalchemy import SQLAlchemy 
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS

app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)
cors = CORS(app, support_credentials = True)



import FlaskTemplate.views
