from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from config import *
import os

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_string = f"postgresql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_URL')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_string

SQLAlchemy = SQLAlchemy
sqlalchemy = sqlalchemy