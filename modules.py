from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db_string = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///jobs.db"
login_manager.init_app(app)

SQLAlchemy = SQLAlchemy
