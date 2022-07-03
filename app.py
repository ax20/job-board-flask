from modules import app, SQLAlchemy, login_manager, bcrypt
from models import Job, User, EmailList, db
from flask import jsonify, request, render_template, redirect, abort, url_for
import markdown, json, os, markdown
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

# Configuration file
with open('site.config.json', 'r') as f:
    site_data = json.load(f)

# Define tokens
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

"""
When the user enters the page they land on the email wall
- If the email is in the database, they are redirected to the job listings page
"""

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=30)])
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)])
    email = StringField(validators=[InputRequired(), Length(min=4, max=30)])
    submit = SubmitField("Register")

    def validate_username(self, username):
        exisiting_username = User.query.filter_by(username=username.data).first()
        if exisiting_username:
            raise ValidationError("That username already exists. Please choose a different one ")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=30)])
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)])
    submit = SubmitField("Login")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_required
@app.route('/')
def index():
    return render_template('index.html', config=site_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
    return render_template('login.html', form=form , config=site_data)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    errors = None
    print(User.query.all())
    
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        errors = form.errors
    return render_template('register.html', form=form, config=site_data, errors=errors)
