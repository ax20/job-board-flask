from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from config import *

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_string = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_URL}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = db_string

SQLAlchemy = SQLAlchemy
sqlalchemy = sqlalchemy

# Database access