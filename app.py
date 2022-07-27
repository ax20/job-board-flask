from modules import app, login_manager, bcrypt, db
from flask import render_template, redirect, url_for, request, session
from models import User, Job, Email
from api import *
import requests
from flask_login import login_required, current_user, logout_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, Email
REGISTER_URL = '/register/'

with open('site.json') as f:
    config = json.load(f)
    f.close()

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

@app.route('/')
def home():
    return render_template('home.jinja2')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = []
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                if user.is_administrator:
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('home'))
            else:
                errors.append("You have entered an invalid password, please try again")
        else:
            errors.append("You have entered an invalid email, please try again")
    else:
        errors.append(form.errors)
    
    # bandage fix to error page
    errors = [] if str(errors) == "[{}]" else errors

    return render_template('login.jinja2', form=form , errors=errors)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    errors = None
    
    if current_user.is_authenticated:
        if current_user.is_administrator:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('home'))

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if is_system_admin(form.email.data):
            user = User(email=form.email.data, password=hashed_password, is_administrator=True)
            db.session.add(user)
        else:
            user = User(email=form.email.data, password=hashed_password, is_administrator=False)
            db.session.add(user)
        
        db.session.commit()
        return redirect(url_for('login'))
    else:
        errors = form.errors

    print(errors)
    return render_template('register.jinja2', form=form, errors=errors)


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard/')
@login_required
def dashboard():
    if current_user.is_administrator:
        return render_template('dashboard.jinja2')
    else:
        return redirect(url_for('home'))