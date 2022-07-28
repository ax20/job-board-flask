from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import sys, json
login_manager = LoginManager()


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
BYPASS_TOKEN = "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8"