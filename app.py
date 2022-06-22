from modules import app, sqlalchemy, SQLAlchemy
from models import Job, db, User
import traceback # ! DEBUG
from flask import jsonify, render_template, request, abort, redirect
import datetime, json
import os
from creds import ACCESS_TOKEN
# Load Site Configurations
with open('site.json', 'r') as f:
    site_data = json.load(f)

def has_posting_expired(job):
    return job.expires_on < datetime.datetime.now()

def purge_jobs():
    for (job) in Job.query.all():
        if has_posting_expired(job):
            delete_job(job.id)

def new_job(model):
    try:
        db.session.add(model)
        db.session.commit()
    except Exception as e:
        print(f"Error adding job: {e}")
        with open('db_creation.log', 'w') as f:
            f.write(traceback.format_exc())

def modify_job(id, new_model):
    try:
        job = Job.query.filter_by(id=id).first()
        job.posted_on = new_model.posted_on
        job.expires_on = new_model.expires_on
        job.title = new_model.title
        job.summary = new_model.summary
        job.description = new_model.description
        job.company = new_model.company
        job.location = new_model.location
        job.url = new_model.url
        job.position = new_model.position
        db.session.commit()
    except Exception as e:
        print(f"Error modifying job: {e}")
        with open('db_creation.log', 'w') as f:
            f.write(traceback.format_exc())

def delete_job(id):
    try:
        job = Job.query.filter_by(id=id).first()
        db.session.delete(job)
        db.session.commit()
    except Exception as e:
        print(f"Error deleting job: {e}")
        with open('db_creation.log', 'w') as f:
            f.write(traceback.format_exc())
        return abort(404)

@app.route('/new/', methods=['POST'])
def new():
    if request.method =="POST":
        new_posting = Job(
            posted_on = datetime.datetime.now().strftime("%d/%m/%y"),
            expires_on = datetime.datetime.strptime(request.form['expires_on'], '%Y-%m-%d'),
            title = request.form['title'],
            summary = request.form['summary'],
            description = request.form['description'],
            company = request.form['company'],
            location = request.form['location'],
            url = request.form['url'],
            position = request.form['position']
        )
        try:
            new_job(new_posting)
        except Exception as e:
            print(f"Error adding job: {e}")
            with open('db_creation.log', 'w') as f:
                f.write(traceback.format_exc())
            abort(500)

        return redirect('/')
    else:
        return "Error"

@app.route('/edit/', methods=['POST'])
def edit():
    posted_on = datetime.datetime.strptime(request.form['posted_on'], '%Y-%m-%d')
    expires_on = datetime.datetime.strptime(request.form['expires_on'], '%Y-%m-%d')
    title = request.form['title']
    summary = request.form['summary']
    description = request.form['description']
    company = request.form['company']
    location = request.form['location']
    url = request.form['url']
    position = request.form['position']
    new_posting = Job(posted_on, expires_on, title, summary, description, company, location, url)
    modify_job(request.form['id'], new_posting)
    return ""

@app.route('/delete/', methods=['POST'])
def delete():
    return delete_job(request.form['id'])

@app.route('/search/<string:args>', methods=['GET'])
def search(args):
    if request.method == "GET":
        search_results = Job.query.filter(Job.title.like(f"%{args}%")).all()
        if len(search_results) > 0:
            results = []
            for result in search_results:
                r = {
                    "id": result.id,
                    "posted_on": result.posted_on,
                    "expires_on": result.expires_on,
                    "title": result.title,
                    "summary": result.summary,
                    "description": result.description,
                    "company": result.company,
                    "location": result.location,
                    "url": result.url,
                    "position": result.position
                }
            results.append(r)
            return jsonify(results)
        else:
            return jsonify([])
    else:
        abort(405)

@app.route('/', methods=['GET'])
def index():
    jobs = Job.query.all()
    filtered_jobs = [job for job in jobs if not has_posting_expired(job)]
    for job in filtered_jobs:
        job.posted_on = job.posted_on.strftime("%d/%m/%y")

    return render_template('index.html', jobs=filtered_jobs, config=site_data)

@app.route('/job/<int:id>/', methods=['GET'])
def job(id):
    job = Job.query.filter_by(id=id).first()
    if job is None:
        abort(404)
    if has_posting_expired(job):
        return abort(410)
    job.posted_on = job.posted_on.strftime('%B, %d, %Y')
    job.expires_on = job.expires_on.strftime('%B, %d, %Y')
    return render_template('job.html', job=job, config=site_data)

@app.route('/purge/<string:password>/', methods=['GET'])
def purge(password):
    if password == ACCESS_TOKEN:
        purge_jobs()
        return redirect('/dashboard/' + password)
    else:
        return abort(500)

@app.route('/dashboard/<string:password>/', methods=['GET'])
def dashboard(password):
    if password:
        if password == ACCESS_TOKEN:
            return render_template('dashboard.html', config=site_data)
        return abort(401)
    return abort(404)

if __name__ == '__main__':
    app.run()