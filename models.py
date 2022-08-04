import traceback
from modules import db
from sqlalchemy import Column, Integer, String, Boolean
from flask_login import UserMixin
from nanoid import generate
from util import logger
class Job(db.Model):
    __tablename__ = 'job_listings'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    unique = Column(String(10), unique=True, nullable=False)
    title = Column(String(100), nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    date_published = Column(String, nullable=False)
    date_updated = Column(String, nullable=False)
    date_expired = Column(String, nullable=True)
    company = Column(String, nullable=False)
    salary = Column(String, nullable=True)
    location = Column(String, nullable=True)
    position = Column(String, nullable=False)
    url = Column(String, nullable=False)
    content = Column(String, nullable=False)

    def __init__(self, unique,  title, content, type, status, date_published, date_updated, date_expired, company, salary, location, position, url):
        self.title = title
        self.unique = unique
        self.content = content
        self.type = type
        self.status = status
        self.date_published = date_published
        self.date_updated = date_updated
        self.date_expired = date_expired
        self.company = company
        self.salary = salary
        self.location = location
        self.position = position
        self.url = url
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'unique': self.unique,
            'content': self.content,
            'title': self.title,
            'type': self.type,
            'status': self.status,
            'date_published': self.date_published,
            'date_updated': self.date_updated,
            'date_expired': self.date_expired,
            'company': self.company,
            'salary': self.salary,
            'location': self.location,
            'position': self.position,
            'url': self.url
        }

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    password = Column(String(100), nullable=False)
    email = Column(String, nullable=False)
    is_administrator = Column(Boolean, nullable=False, default=False)

    def __init__(self, email, password, is_administrator):
        self.password = password
        self.email = email
        self.is_administrator = is_administrator

    @property
    def serialize(self):
        return {
            'id': self.id,
            'email': self.email,
            'is_administrator': self.is_administrator
        }

class Email(db.Model):
    __tablename__ = 'email_list'
    __table_args__ = {'extend_existing': True}

    email = Column(String, nullable=False, unique=True, primary_key=True)

    def __init__(self, email):
        self.email = email

    @property
    def serialize(self):
        return {
            'email': self.email
        }

def create_tables():
    try:
        db.create_all()
        print('✔️ Initalized database successfully.')
    except Exception as e:
        logger(traceback.format_exc())