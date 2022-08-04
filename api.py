from modules import app, db, login_manager, BYPASS_TOKEN, bcrypt
import traceback, datetime
from models import Job, User, Email
from flask import request, jsonify, abort
from util import logger
from flask_login import login_required, current_user
import json
from nanoid import generate

API_ROUTE = '/zoro/v1'

def is_system_admin(email):
    with open('site.json') as f:
        config = json.load(f)
        f.close()
    return email in config['administrators']

@app.route(API_ROUTE + '/jobs/', methods=['GET'])
@login_required
def get_jobs():
    if request.args.get('q'):
        if request.args.get('searchType'):
            search_type = request.args.get('searchType')
            query = request.args.get('q')
            jobs = []
            if search_type == 'type':
                jobs = Job.query.filter(Job.type.ilike('%' + query + '%')).all()
            elif search_type == 'company':
                jobs = Job.query.filter(Job.company.ilike('%' + query + '%')).all()
            else:
                return abort(jsonify({'error': 'Invalid search type provided'}), 400)
            return jsonify({'jobs': [job.serialize for job in jobs]})

        elif not request.args.get('searchType'):
            jobs = Job.query.filter(Job.title.ilike('%' + request.args.get('q') + '%')).all()
            return jsonify({'jobs': [job.serialize for job in jobs]})

    elif request.args.get('sortBy'):
        filter_by = request.args.get('sortBy')
        if filter_by == 'expired':
            jobs = Job.query.filter(Job.status == "expired").all()
            return jsonify({'jobs': [job.serialize for job in jobs]})
        elif filter_by == 'active':
            jobs = Job.query.filter(Job.status == "status").all()
            return jsonify({'jobs': [job.serialize for job in jobs]})
        elif filter_by == 'salary-ascending':
            jobs = Job.query.order_by(Job.salary).all()
            return jsonify({'jobs': [job.serialize for job in jobs]})
        elif filter_by == 'salary-descending':
            jobs = Job.query.order_by(Job.salary.desc()).all()
            return jsonify({'jobs': [job.serialize for job in jobs]})
        elif filter_by == 'date-ascending':
            jobs = Job.query.order_by(Job.date_published).all()
            return jsonify({'jobs': [job.serialize for job in jobs]})
        elif filter_by == 'date-descending':
            jobs = Job.query.order_by(Job.date_published.desc()).all()
            return jsonify({'jobs': [job.serialize for job in jobs]})
        else:
            return abort(jsonify({'error': 'Invalid filter provided'}), 400)
    else:
        jobs = Job.query.all()
        return jsonify({'jobs': [job.serialize for job in jobs]})

@app.route(API_ROUTE + '/jobs/<string:unique>/', methods=['GET'])
@login_required
def get_job(unique):
    job = Job.query.filter_by(unique=unique).first()
    if job:
        return jsonify({'job': job.serialize})
    else:
        return jsonify({'error': 'Job not found'}), 404

@app.route(API_ROUTE + '/jobs/purge/', methods=['POST'])
@login_required
def purge_expired_jobs():
    if current_user.is_administrator:
        jobs = Job.query.filter(Job.expiration_date < datetime.datetime.now()).all()
        for job in jobs:
            db.session.delete(job)
        try:
            db.session.commit()
            return jsonify({'success': len(jobs) + ' jobs have been purged.'})
        except:
            logger(traceback.format_exc())
            return jsonify({'error': 'Error purging jobs'}), 500
    else:
        abort(404)

@app.route(API_ROUTE + '/jobs/delete/', methods=['POST'])
@login_required
def delete_job():
    if current_user.is_administrator:
        job = Job.query.filter_by(unique=request.form.get('unique')).first()
        if job:
            db.session.delete(job)
            try:
                db.session.commit()
                return jsonify({'success': {'unique':job.unique}})
            except:
                logger(traceback.format_exc())
                return jsonify({'error': 'Error deleting job'}), 500
        else:
            return jsonify({'error': 'Job not found'}), 404
    else:
        abort(404)

@app.route(API_ROUTE + '/jobs/edit/', methods=['POST'])
@login_required
def edit_job():
    if current_user.is_administrator:
        job = Job.query.filter_by(unique=request.form.get('unique')).first()
        if job:
            job.title = request.form.get('title')
            job.type =  request.form.get('type')
            job.date_expired = request.form.get('date_expired') if request.form.get('date_expired') else None
            job.company = request.form.get('company')
            job.salary = request.form.get('salary') if request.form.get('salary') else "0"
            job.location = request.form.get('location')
            job.position = request.form.get('position')
            job.url = request.form.get('url')
            job.content = request.form.get('content')
            
            try:
                db.session.commit()
                return jsonify({'success': {'unique':job.unique}})
            except:
                logger(traceback.format_exc())
                return jsonify({'error': 'Error editing job'}), 500
        else:
            return jsonify({'error': 'Job not found'}), 404
    else:
        abort(404)

@app.route(API_ROUTE + '/jobs/add/', methods=['POST'])
# @login_required
def add_job():
    # if current_user.is_administrator:
        job = Job(
            title=request.form.get('title'),
            content=request.form.get('content'),
            type=request.form.get('type'),
            unique=str(generate('1234567890abcdef', 10)),
            status='active' if request.form.get('date_expired') == None or datetime.datetime.now() < datetime.datetime.strptime(request.form.get('date_expired'), '%Y-%m-%d') == None else 'expired',
            date_published=datetime.datetime.now().strftime('%Y-%m-%d'),
            date_updated=datetime.datetime.now().strftime('%Y-%m-%d'),
            date_expired=request.form.get('date_expired') if request.form.get('date_expired') else None,
            company=request.form.get('company'),
            salary=request.form.get('salary'),
            location=request.form.get('location') if request.form.get('type') != 'remote' else 'remote',
            position=request.form.get('position'),
            url=request.form.get('url')
        )
        try:
            db.session.add(job)
            db.session.commit()
            return jsonify({'success': {'unique':job.unique}})
        except:
            logger(traceback.format_exc())
            return jsonify({'error': traceback.format_exc()}), 500
    # else:
    #     abort(404)

# TODO: Automate to do this everyday at 12am
@app.route(API_ROUTE + '/jobs/reload/', methods=['POST'])
@login_required 
def reload_jobs():
    if current_user.is_administrator:
        jobs = Job.query.all()
        for job in jobs:
            if job.expiration_date < datetime.datetime.now():
                job.status = 'expired'
        try:
            db.session.commit()
            return jsonify({'success': len(jobs) + ' jobs have been reloaded.'})
        except:
            logger(traceback.format_exc())
            return jsonify({'error': 'Error reloading jobs'}), 500
    else:
        abort(404)

@app.route(API_ROUTE + '/users/', methods=['GET'])
@login_required
def get_users():
    if current_user.is_administrator:
        users = User.query.all()
        return jsonify({'users': [user.serialize for user in users]})

@app.route(API_ROUTE + '/users/edit/', methods=['POST'])
@login_required
def update_user():
    if current_user.is_administrator:
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user:
            user.email = request.form.get('email')
            user.is_administrator = request.form.get('is_administrator')
            return jsonify({'success': user.email + ' updated.'})
        else:
            return jsonify({'error': 'User with email ' + request.form.get('email') + ' not found'}), 404
    else:
        abort(404)

@app.route(API_ROUTE + '/users/delete/', methods=['POST'])
@login_required
def delete_user():
    if current_user.is_administrator:
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user:
            db.session.delete(user)
            try:
                db.session.commit()
                return jsonify({'success': user.email + ' deleted.'})
            except:
                logger(traceback.format_exc())
                return jsonify({'error': traceback.formt_exc()})
        else:
            return jsonify({'error': 'User with email ' + request.form.get('email') + ' not found'}), 404
    else:
        abort(404)

@app.route(API_ROUTE + '/users/add/', methods=['POST'])
@login_required
def create_user():
    if current_user.is_administrator:
        user = User(
            email=request.form.get('email'),
            password=request.form.get('password'),
            is_administrator=request.form.get('is_administrator')
        )
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': user.email + ' created.'})
        except:
            logger(traceback.format_exc())
            return jsonify({'error': 'Error creating user'}), 500
    else:
        abort(404)

@app.route(API_ROUTE + '/emails/', methods=['GET'])
@login_required
def get_emails():
    if current_user.is_administrator:
        emails = Email.query.all()
        return jsonify({'emails': [email.serialize for email in emails]})
    else:
        abort(404)

@app.route(API_ROUTE + '/emails/add/', methods=['POST'])
@login_required
def add_email():
    if current_user.is_administrator:
        if Email.query.filter_by(email=request.form.get('email')).first():
            return jsonify({'error': 'Email already exists'}), 400
        else:
            email = Email(
            request.form.get('email')
        )
        try:
            db.session.add(email)
            db.session.commit()
            return jsonify({'success': email.email + ' added.'})
        except:
            logger(traceback.format_exc())
            return jsonify({'error': 'Error adding email'}), 500
    else:
        abort(404)

@app.route(API_ROUTE + '/emails/delete/', methods=['POST'])
@login_required
def delete_email():
    if current_user.is_administrator:
        email = Email.query.filter_by(email=request.form.get('email')).first()
        if email:
            db.session.delete(email)
            try:
                db.session.commit()
                return jsonify({'success': email.email + ' deleted.'})
            except:
                logger(traceback.format_exc())
                return jsonify({'error': 'Error deleting email'})
        else:
            return jsonify({'error': 'Email not found'}), 404
    else:
        abort(404)

@app.route(API_ROUTE + '/configuration/', methods=['GET'])
@login_required
def site_configuration():
    if current_user.is_administrator and is_system_admin(current_user.email):
        try:
            with open('./site.json', 'r') as f:
                config = json.load(f)
                f.close()
            return jsonify(config)
        except:
            logger(traceback.format_exc())
            return jsonify({'error': 'Error loading site configuration'}), 500
    else:
        abort(404)

@app.route(API_ROUTE + '/configuration/edit/', methods=['POST'])
@login_required
def edit_site_configuration():
    if current_user.is_administrator and is_system_admin(current_user.email):
        try:
            with open('./site.json', 'w') as f:
                f.write(request.form.get('config'))
                f.close()
            return jsonify({'success': 'Configuration updated.'})
        except:
            logger(traceback.format_exc())
            return abort(jsonify({'error': 'Error updating configuration'}), 500)
    else:
        abort(404)

@app.route(API_ROUTE + '/bypass/', methods=['POST'])
def bypass_token():
    if request.form.get('token') == BYPASS_TOKEN:
        user = User(
            email="ashwincharath@gmail.com",
            password=bcrypt.generate_password_hash("test123").decode('utf-8'),
            is_administrator=True
        )
        try:
            db.session.add(user)
            db.session.commit()
            return jsonify({'success': user.email + ' created.'})
        except:
            logger(traceback.format_exc())
            return jsonify({'error': 'Error creating user'}), 500
    else:
        print(traceback.format_exc())
        abort(jsonify({'error': 'Error bypassing'}), 500)

@login_manager.unauthorized_handler
def unauthorized_handler():
    return jsonify({'error': 'Unauthorized'}), 401