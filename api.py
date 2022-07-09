from cmath import log
from modules import app
from models import Job, db, User
import traceback, datetime, os
from flask import jsonify, request, redirect
from flask_login import login_required, current_user

# ACCESS_TOKEN
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

def error_log(message):
    with open('error_log.log', 'a') as f:
        f.write(message + '\n')

def is_expired(job):
    return job.date_expiry < datetime.datetime.now()

@login_required
@app.route('/purge/', methods=['POST'])
def purge_jobs():
    if current_user.isAdmin:
        jobs = Job.query.all()
        for job in jobs:
            if is_expired(job):
                db.session.delete(job)
        db.session.commit()
        return jsonify({'success': 'Jobs purged'}), 200
    else:
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

@login_required
@app.route('/new/', methods=['POST'])
def new_job():
    if current_user.isAdmin:
        new_job = Job(
            date_expiry = datetime.datetime.strptime(request.form['date_expiry'], '%Y-%m-%d'),
            title = request.form['title'],
            preview = request.form['preview'],
            content = request.form['content'],
            company = request.form['company'],
            location = request.form['location'],
            url = request.form['url'],
            position = request.form['position']
        )

        try:
            db.session.add(new_job)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            error_log(traceback.format_exc())
            return jsonify({'error': 'Error adding job'}), 500

@login_required
@app.route('/edit/', methods=['POST'])
def edit_job():
    if current_user.isAdmin:
        job = Job.query.filter_by(id=request.form['id']).first()
        job.date_modified = datetime.datetime.now()
        job.date_expiry = job.date_expiry if request.form['date_expiry'] == '' else datetime.datetime.strptime(request.form['date_expiry'], '%Y-%m-%d')
        job.title = job.title if request.form['title'] == '' else request.form['title']
        job.preview = job.preview if request.form['preview'] == '' else request.form['preview']
        job.content = job.content if request.form['content'] == '' else request.form['content']
        job.company = job.company if request.form['company'] == '' else request.form['company']
        job.location = job.location if request.form['location'] == '' else request.form['location']
        job.url = job.url if request.form['url'] == '' else request.form['url']
        job.position = job.position if request.form['position'] == '' else request.form['position']
        
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            error_log(traceback.format_exc())
            return jsonify({'error': 'Error editing job'}), 500
    else:
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

@login_required
@app.route('/delete/', methods=['POST'])
def delete_job():
    if current_user.isAdmin:
        job = Job.query.filter_by(id=request.form['id']).first()
        db.session.delete(job)
        db.session.commit()
        return redirect('/')
    else:
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

@login_required
@app.route('/search/', methods=['GET'])
def search():
    if request.args.get('q'):
        jobs = Job.query.filter(Job.title.ilike('%' + request.args.get('q') + '%')).all()
        return jsonify({'results': [job.serialize() for job in jobs]})
    else:
        return jsonify({'error': 'No search query provided'}), 400

@login_required
@app.route('/config/', methods=['POST'])
def config():
    if current_user.isAdmin:
        config = request.form['config']
        with open('static/site_config.json', 'w') as f:
            f.write(config)
        return jsonify({'success': 'Configuration updated'}), 200
    else:
        return jsonify({'error': 'You are not authorized to perform this action'}), 403

@login_required
@app.route('/users/', methods=['GET', 'POST'])
def users():
    if current_user:
        if request.method == 'POST':
            user = User.query.filter_by(email=request.form['email']).first()
            user.isAdmin = request.form['isAdmin']
            db.session.commit()
            return redirect('/user/')
        elif request.method == 'GET':
            users = User.query.all()
            print(users)
            if len(users) != 0:
                return jsonify({'users': [user.serialize() for user in users]})
            else:
                return jsonify({'error': 'No users found'}), 404
    else:
        return jsonify({'error': 'You are not authorized to perform this action'}), 403