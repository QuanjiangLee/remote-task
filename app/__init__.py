import os
from flask import Flask
from flask_login import LoginManager
from config import basedir
from flask_sqlalchemy import SQLAlchemy
#from flask_assets import assets
#from flask_bcrypt import bcrypt

app = Flask(__name__)    #app instance
#from app import routes   #'app' module
#from app import views
app.config.from_object('config') #app configuration file
db = SQLAlchemy(app)
LoginMa = LoginManager()
LoginMa.init_app(app)
LoginMa.login_view = 'login' 

from app import forms, views, models
