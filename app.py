from modules import app, sqlalchemy, SQLAlchemy
from models import Job, db
import traceback # ! DEBUG
from flask import render_template, request, abort
import datetime

# add jobe model to db
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


@app.route('/', methods=['GET'])
def index():
    jobs = Job.query.all()
    return render_template('index.html', jobs=jobs)

@app.route('/new', methods=['POST'])
def new():
    posted_on = datetime.datetime.now()
    expires_on = posted_on + datetime.timedelta(days=7)
    title = request.form['title']
    summary = request.form['summary']
    description = request.form['description']
    company = request.form['company']
    location = request.form['location']
    url = request.form['url']
    new_posting = Job(posted_on, expires_on, title, summary, description, company, location, url)
    new_job(new_posting)
    return ""