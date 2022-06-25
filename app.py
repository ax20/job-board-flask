from modules import app, SQLAlchemy
from models import Job, db, User
import traceback # ! DEBUG
from flask import jsonify, render_template, request, abort, redirect
import datetime, json, os, markdown

ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

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
        with open('db_creation.log', 'a') as f:
            f.write(traceback.format_exc())

def modify_job(id, new_model):
    try:
        job = Job.query.filter_by(id=id).first()
        job.posted_on = new_model.posted_on if new_model.posted_on != None else job.posted_on
        job.expires_on = new_model.expires_on if new_model.expires_on != "" else job.expires_on
        job.title = new_model.title if new_model.title != "" else job.title
        job.description = new_model.description if new_model.description != "" else job.description
        job.summary = new_model.summary if new_model.summary != "" else job.summary
        job.location = new_model.location if new_model.location != "" else job.location
        job.company = new_model.company if new_model.company != "" else job.company
        job.url = new_model.url if new_model.url != "" else job.url
        db.session.commit()
    except Exception as e:
        print(f"Error modifying job: {e}")
        with open('db_creation.log', 'a') as f:
            f.write(traceback.format_exc())

def delete_job(id):
    try:
        job = Job.query.filter_by(id=id).first()
        db.session.delete(job)
        db.session.commit()
    except Exception as e:
        print(f"Error deleting job: {e}")
        with open('db_creation.log', ) as f:
            f.write(traceback.format_exc())
        return abort(404)

@app.route('/new/', methods=['POST'])
def new():
    if request.method =="POST":
        new_posting = Job(
            posted_on = datetime.datetime.now(),
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
            with open('db_creation.log', ) as f:
                f.write(traceback.format_exc())
            abort(500)

        return redirect('/')
    else:
        return "Error"

@app.route('/edit/', methods=['POST'])
def edit():
    fposted_on = "" if request.form['posted_on'] == None else datetime.datetime.strptime(request.form['posted_on'], '%Y-%m-%d')
    fexpires_on = "" if request.form['expires_on'] == None else datetime.datetime.strptime(request.form['expires_on'], '%Y-%m-%d')
    ftitle = "" if request.form['title'] == None else request.form['title']
    fsummary = "" if request.form['summary'] == None else request.form['summary']
    fdescription =   "" if request.form['description'] == None else request.form['description']
    fcompany = "" if request.form['company'] == None else request.form['company']
    flocation = "" if request.form['location'] == None else request.form['location']
    furl = "" if request.form['url'] == None else request.form['url']
    fposition = "" if request.form['position'] == None else request.form['position']
    new_posting = Job(posted_on=fposted_on, position=fposition, expires_on=fexpires_on, title=ftitle, summary=fsummary, description=fdescription, company=fcompany, location=flocation, url=furl)
    modify_job(request.form['id'], new_posting)
    return redirect('/')

@app.route('/delete/', methods=['POST'])
def delete():
    return delete_job(request.form['id'])

@app.route('/search/<string:args>', methods=['GET'])
def search(args):
    if request.method == "GET":
        search_results = Job.query.filter(Job.title.like(f"%{args}%")).all()
        if len(search_results) > 0:
            results = ""
            for result in search_results:
                results+=f"<li class='w-full my-2'><a class='rounded-lg p-3 bg-slate-50 dark:bg-gray-600' href='/job/{result.id}'>{result.title}</a></li>"
            return results
        else:
            return jsonify([])
    else:
        abort(405)

@app.route('/', methods=['GET'])
def index():
    if request.method == "GET":
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
    job.description = markdown.markdown(job.description)

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