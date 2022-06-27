from modules import app, SQLAlchemy
from sqlalchemy import Integer, String, Column, DateTime
from flask_wtf import wtforms
from flask_login import UserMixin
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

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

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kaw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        exisiting_username = User.query.filter_by(username=username.data).first()
        if exisiting_username:
            raise ValidationError("That username already exists. Please choose a different one ")

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=30)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)], render_kaw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        exisiting_username = User.query.filter_by(username=username.data).first()
        if exisiting_username:
            raise ValidationError("That username already exists. Please choose a different one ")


class EmailList(db.Model):
    __tablename__ = 'email_list'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False)

    def __init__(self, email):
        self.email = email