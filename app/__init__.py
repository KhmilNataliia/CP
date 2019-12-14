import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine
from flask_pymongo import PyMongo

# local imports
from flask_login import LoginManager

# db variable initialization
db = SQLAlchemy()
mdb = MongoEngine()

login_manager = LoginManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Vac3314147@localhost/carpaintsystem'
#app.config['MONGODB_SETTINGS'] = {'db': 'MyCrawl', 'alias': 'default'}
app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/MyCrawl'
app.config['MONGO_DBNAME'] = 'MyCrawl'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/MyCrawl'

mongo = PyMongo(app)

mdb.init_app(app)
db.init_app(app)
bcrypt = Bcrypt(app)

login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "signin"

from app import routes

