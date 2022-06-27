from modules import app, SQLAlchemy, login_manager
from models import Job, User, EmailList

from flask import jsonify, request, render_template, redirect, abort
import markdown, json, os, markdown

# Define tokens
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN')

"""
When the user enters the page they land on the email wall
- If the email is in the database, they are redirected to the job listings page
"""

@app.route('/')
def index():
    return render_template('index.html')