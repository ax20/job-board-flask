from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

login_manager = LoginManager()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret'
db_string = f"sqlite://jobs.db"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///jobs.db"
login_manager.init_app(app)
bcrypt = Bcrypt(app)

SQLAlchemy = SQLAlchemy
