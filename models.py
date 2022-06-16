from modules import app, SQLAlchemy
from sqlalchemy import Integer, String, Column, DateTime
import traceback # ! DEBUG


db = SQLAlchemy(app)

class Job(db.Model):
    __tablename__ = 'jobs'
    __tableargs__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    posted_on = Column(DateTime, nullable=False)
    expires_on = Column(DateTime, nullable=False)
    title = Column(String(100), nullable=False)
    summary = Column(String(1000), nullable=False)
    description = Column(String(10000), nullable=False)
    company = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    url = Column(String(100), nullable=False)
    position = Column(String(100), nullable=False)

    def __init(self, posted_on, expires_on, title, summary, description, company, location, url, position):
        self.posted_on = posted_on
        self.expires_on = expires_on
        self.title = title
        self.summary = summary
        self.description = description
        self.company = company
        self.location = location
        self.url = url
        self.position = position

class User(db.Model):
    __tablename__ = 'users'
    __tableargs__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

def create_all():
    try:
        db.create_all()
        print("Created database")
    except Exception as e:
        print(f"Error creating database: {e}")
        with open('db_creation.log', 'a') as f:
            f.write(traceback.format_exc())