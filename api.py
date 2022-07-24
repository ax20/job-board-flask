from webbrowser import get
from modules import app, db
import traceback, datetime
from models import Job, User, Email
from flask import request, jsonify, abort
from util import logger

API_ROUTE = '/zoro/v1'

@app.route(API_ROUTE + '/jobs/', methods=['GET'])
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
    else:
        jobs = Job.query.all()
        return jsonify({'jobs': [job.serialize for job in jobs]})

@app.route(API_ROUTE + '/jobs/<string:unique>/', methods=['GET'])
def get_job(unique):
    job = Job.query.filter_by(unique=unique).first()
    if job:
        return jsonify({'job': job.serialize})
    else:
        return abort(jsonify({'error': 'Job not found'}), 404)

@app.route(API_ROUTE + '/jobs/purge/', methods=['POST'])
def purge_expired_jobs():
    jobs = Job.query.filter(Job.expiration_date < datetime.datetime.now()).all()
    for job in jobs:
        db.session.delete(job)
    try:
       db.session.commit()
       return jsonify({'success': len(jobs) + ' jobs have been purged.'})
    except:
        logger(traceback.format_exc())
        return abort(jsonify({'error': 'Error purging jobs'}), 500)

@app.route(API_ROUTE + '/jobs/delete/', methods=['POST'])
def delete_job():
    job = Job.query.filter_by(unique=request.form.get('unique')).first()
    if job:
        db.session.delete(job)
        try:
            db.session.commit()
            return jsonify({'success': job.unique + ' deleted.'})
        except:
            logger(traceback.format_exc())
            return abort(jsonify({'error': 'Error deleting job'}), 500)
    else:
        return abort(jsonify({'error': 'Job not found'}), 404)

@app.route(API_ROUTE + '/jobs/edit/', methods=['POST'])
def edit_job():
    job = Job.query.filter_by(unique=request.form.get('unique')).first()
    if job:
        job.title = request.form.get('title')
        job.type =  request.form.get('type')
        job.status = request.form.get('status')
        job.date_published = request.form.get('date_published')
        job.date_updated = request.form.get('date_updated')
        job.date_expired = request.form.get('date_expired') if request.form.get('date_expired') else None
        job.company = request.form.get('company')
        job.salary = request.form.get('salary') if request.form.get('salary') else None
        job.location = request.form.get('location')
        job.position = request.form.get('position')
        job.url = request.form.get('url')
        try:
            db.session.commit()
            return jsonify({'success': job.unique + ' edited.'})
        except:
            logger(traceback.format_exc())
            return abort(jsonify({'error': 'Error editing job'}), 500)
    else:
        return abort(jsonify({'error': 'Job not found'}), 404)

@app.route(API_ROUTE + '/jobs/add/', methods=['POST'])
def add_job():
    job = Job(
        title=request.form.get('title'),
        content=request.form.get('content'),
        type=request.form.get('type'),
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
        return jsonify({'success': job.unique + ' added.'})
    except:
        logger(traceback.format_exc())
        return abort(jsonify({'error': traceback.format_exc()}), 500)

@app.route(API_ROUTE + '/jobs/reload/', methods=['POST']) 
def reload_jobs():
    jobs = Job.query.all()
    for job in jobs:
        if job.expiration_date < datetime.datetime.now():
            job.status = 'expired'
    try:
        db.session.commit()
        return jsonify({'success': len(jobs) + ' jobs have been reloaded.'})
    except:
        logger(traceback.format_exc())
        return abort(jsonify({'error': 'Error reloading jobs'}), 500)

# Users

@app.route(API_ROUTE + '/users/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.serialize for user in users]})

@app.route(API_ROUTE + '/users/edit/', methods=['POST'])
def update_user():
    user = User.query.filter_by(email=request.form.get('email')).first()
    if user:
        user.email = request.form.get('email')
        user.is_administrator = request.form.get('is_administrator')
    else:
        return abort(jsonify({'error': 'User with email ' + request.form.get('email') + ' not found'}), 404)

@app.route(API_ROUTE + '/users/delete/', methods=['POST'])
def delete_user():
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
        return abort(jsonify({'error': 'User with email ' + request.form.get('email') + ' not found'}), 404)

@app.route(API_ROUTE + '/users/add/', methods=['POST'])
def create_user():
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
        return abort(jsonify({'error': 'Error creating user'}), 500)

@app.route(API_ROUTE + '/emails/', methods=['GET'])
def get_emails():
    emails = Email.query.all()
    return jsonify({'emails': [email.serialize for email in emails]})