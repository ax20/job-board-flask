from modules import app, login_manager, bcrypt, db
from models import User, Job, Email
from api import *
import requests
from flask_login import login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, Email
REGISTER_URL = '/register/'

def is_system_admin(email):
    r = requests.get('/api/configuration/')
    if r.status_code == 200:
        for admin in r.json()['administrators']:
            if email == admin:
                return True
        return False

    raise Exception('Failed to get system administrators, check site.json')

class RegisterForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)])
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Email already registered.')

class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField('Login')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))