from urllib import response
import requests, json, sys, traceback
from models import create_tables
from modules import BYPASS_TOKEN

api_url = 'http://localhost:5000/zoro/v1'

def add_jobs():
    with open('test_jobs.json') as json_file:
        data = json.load(json_file)
        json_file.close()
    
    for job in data:
        try:
            response = requests.post(api_url + '/jobs/add/', data=job)
            if response.status_code == 200:
                print('✔️ POST /zoro/v1/jobs/add/')
                print(response.text)
            else:
                print('❌ POST /zoro/v1/jobs/add/, returned ', response.status_code)
                print(response.text)
                sys.exit(1)
        except:
            print('❌ POST /zoro/v1/jobs/add/ REFUSED')

def f():
    create_tables()
    print('✔️ Setup database')
    sys.exit(0)

def setup_database():

    create_tables()

    with open('test_jobs.json') as json_file:
        data = json.load(json_file)
        json_file.close()
    
    try:
        user = requests.post(api_url + '/bypass/', data={'token': BYPASS_TOKEN})
        if user.status_code == 200:
            print('✔️ POST /zoro/v1/bypass/')
        else:
            print('❌ POST /zoro/v1/bypass/, returned ', user.status_code)
            print(user.text)
            sys.exit(1)
    except:
        print('❌ POST /zoro/v1/bypass/ REFUSED')
        print(traceback.format_exc())
        sys.exit(1)

    for job in data:
        try:
            response = requests.post(api_url + '/jobs/add/', data=job)
            if response.status_code == 200:
                print('✔️ POST /zoro/v1/jobs/add/')
                print(response.text)
            else:
                print('❌ POST /zoro/v1/jobs/add/, returned ',response.status_code)
                print(response.text)
                sys.exit(1)
        except:
            print('❌ POST /zoro/v1/jobs/add/ REFUSED')

def check_endpoints():
    
    # GET /zoro/v1/jobs/ (empty)
    try:
        all_jobs = requests.get(api_url + '/jobs/')
        if all_jobs.status_code == 200:
            print('✔️ GET /zoro/v1/jobs/ (empty)')
        else:
            print('❌ GET /zoro/v1/jobs/ (empty), returned ',response.status_code)
            print(all_jobs.text)
    except:
        print('❌ GET /zoro/v1/jobs/ (empty) REFUSED')

     # GET /zoro/v1/jobs/ (query)
    try:
        all_jobs_query = requests.get(api_url + '/jobs/?q=hello&searchBy=content')
        if all_jobs_query.status_code == 200:
            print('✔️ GET /zoro/v1/jobs/ (empty)')
        else:
            print('❌ GET /zoro/v1/jobs/ (empty), returned ',response.status_code)
            print(all_jobs_query.text)
    except:
        print('❌ GET /zoro/v1/jobs/ (empty) REFUSED')

    # GET /zoro/v1/jobs/ (id)
    try:
        job_by_id = requests.get(api_url + '/jobs/' + all_jobs.json()['jobs'][-1]['unique'])
        if job_by_id.status_code == 200:
            print('✔️ GET /zoro/v1/jobs/ (id)')
        else:
            print('❌ GET /zoro/v1/jobs/ (id), returned ',response.status_code)
            print(job_by_id.text)
    except:
        print('❌ GET /zoro/v1/jobs/ (id) REFUSED')

    # POST /zoro/v1/jobs/edit/
    try:
        job_to_edit = all_jobs.json()['jobs'][-1]
        job_to_edit['title'] = 'Hello world'
        job_edited = requests.post(api_url + '/jobs/edit/', data=job_to_edit)
        if job_edited.status_code == 200:
            print('✔️ POST /zoro/v1/jobs/edit/')
        else:
            print('❌ POST /zoro/v1/jobs/edit/, returned ',response.status_code)
            print(job_edited.text)
    except:
        print('❌ POST /zoro/v1/jobs/edit/ REFUSED')

    # GET /zoro/v1/jobs/ (id) (to check if it was edited)
    try:
        job_by_id = requests.get(api_url + '/jobs/' + all_jobs.json()['jobs'][-1]['unique'])
        # if the job has the title Hello World, it was edited
        if job_by_id.json()['title'] == 'Hello world':
            print('✔️ GET /zoro/v1/jobs/ (id) (to check if it was edited)')
        else:
            print('❌ GET /zoro/v1/jobs/ (id) (to check if it was edited), returned ',response.status_code)
            print(job_by_id.text)
    except:
        print('❌ GET /zoro/v1/jobs/ (id) (to check if it was edited) REFUSED')

    # DELETE /zoro/v1/jobs/delete/
    try:
        job_to_delete = all_jobs.json()['jobs'][-1]
        job_deleted = requests.delete(api_url + '/jobs/delete/' + job_to_delete['unique'])
        if job_deleted.status_code == 200:
            print('✔️ DELETE /zoro/v1/jobs/delete/')
        else:
            print('❌ DELETE /zoro/v1/jobs/delete/, returned ',response.status_code)
            print(job_deleted.text)
    except:
        print('❌ DELETE /zoro/v1/jobs/delete/ REFUSED')

if __name__ == '__main__':
    # setup_database()
    # check_endpoints()
    add_jobs()