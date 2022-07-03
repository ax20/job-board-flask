from modules import app, SQLAlchemy
from sqlalchemy import Integer, String, Column, DateTime
from flask_login import UserMixin
import traceback #!! DEBUG

db = SQLAlchemy(app)

class Job(db.Model):
    __tablename__ = 'jobs'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    date_created = Column(DateTime, default=db.func.current_timestamp(), nullable=False)
    date_modified = Column(DateTime, default=db.func.current_timestamp(), nullable=False, onupdate=db.func.current_timestamp())
    date_expiry = Column(DateTime, nullable=False)
    title = Column(String(100), nullable=False) 
    preview = Column(String(500), nullable=True) # one sentence preview of the job 
    content = Column(String(10000), nullable=False) # full description of the job
    company = Column(String(100), nullable=True)
    location = Column(String(100), nullable=True)
    url = Column(String(500), nullable=True)
    position = Column(String(100), nullable=True)

    def __init__(self, title, preview, content, company, location, url, position):
        self.title = title
        self.preview = preview
        self.content = content
        self.company = company
        self.location = location
        self.url = url
        self.position = position

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
class EmailList(db.Model):
    __tablename__ = 'email_list'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)

    def __init__(self, email):
        self.email = email
        
def create_tables():
    try:
        db.create_all()
        print("Created tables")
    except Exception as e:
        print(f"Error creating database: {e}")
        with open('db_creation.log', 'a') as f:
            f.write(traceback.format_exc())