from venv import create
from modules import app, login_manager, bcrypt, db
from flask import render_template, redirect, url_for, request
from models import User, create_tables
from models import Email as EmailList
from api import *
from os import remove, mkdir, path
from sys import exit, stdout
from flask_login import login_required, current_user, logout_user, login_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo, Email
REGISTER_URL = '/register/'

with open('site.json') as f:
    config = json.load(f)
    f.close()

try:
    create_tables()
    
    if User.query.filter_by(email="ashwincharath@gmail.com").first():
        print("user exists")
    else:
        pw = bcrypt.generate_password_hash("password123").decode('utf-8')
        print("generated: " + pw)
        u = User("ashwincharath@gmail.com",pw, True)
        db.session.add(u)
        print("passed: " + u.password)
        db.session.commit()
        u = User.query.filter_by(email="ashwincharath@gmail.com").first()
        print("user: " + u.password)

except Exception as e:
    traceback.print_exc(file=stdout)
    exit(1)

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

class EmailForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Email()])
    submit = SubmitField('Access')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    if request.args.get('errors'):
        return render_template('home.jinja2', errors=request.args.get('errors'))
    return render_template('home.jinja2')

@app.route('/view/<string:unique>/', methods=['GET', 'POST'])
def view(unique):
    if request.method == 'GET':
        job = Job.query.filter_by(unique=unique).first()
        if job:
            return render_template('listing.jinja2', job=job)
        else:
            return abort(404)
    elif request.method == 'POST':
        if current_user.is_administrator:
            job = Job.query.filter_by(unique=unique).first()
            if job:
                return render_template('listing_edit.jinja2', job=job)
            else:
                return abort(404)
        else:
            return redirect("/view/{}".format(unique))
    
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    errors = {}
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            print(user.password)
            print(bcrypt.generate_password_hash("password123").decode('utf-8'))
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                if user.is_administrator:
                    return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('home'))
            else:
                errors['password'] = "You have entered an invalid password, please try again"
        else:
            errors['email'] = "You have entered an invalid email, please try again"
    else:
        errors = dict(errors.items())
        errors.update(form.errors)
    
    # bandage fix to error page
    errors = {} if str(errors) == "[{}]" else errors

    return render_template('login.jinja2', form=form , errors=errors)

# wtf is this for?
@app.route('/email/', methods=['GET', 'POST'])
def email():
    try:
        x = request.args.get('email')
        email = EmailList.query.filter_by(email=x).first()
        print(email)
        return redirect(url_for('register'))
    except Exception as e:
        return str(traceback.format_exc())

@login_required
@app.route('/new/', methods=['GET'])
def create_listing():
    if current_user.is_administrator:
        return render_template('listing_new.jinja2')    

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    errors = []

    if form.validate_on_submit():
        if is_system_admin(form.email.data):
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(email=form.email.data, password=hashed_password, is_administrator=True)
            db.session.add(user)
        else:
            if EmailList.query.filter_by(email=form.email.data).first() != None:
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                user = User(email=form.email.data, password=hashed_password, is_administrator=False)
                db.session.add(user)
            else:
                return redirect(url_for('home'))

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

if __name__ == '__main__':
    if not path.isdir('data'):
        mkdir('data')
        print('Created data directory')

    if path.isfile('data/database.db'):
        remove('data/database.db')
        print('Removed database file')

    with open('data/database.db', 'x') as f:
            f.close()
            print('Created database file')
    app.run()