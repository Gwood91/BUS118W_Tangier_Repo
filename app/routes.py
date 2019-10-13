import sys
from flask import render_template
import os
# change the directory to current user
current_user = user_root = os.path.expanduser('~')
local_path = user_root + "/Tangier"
sys.path.append(local_path)
from app import app


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Christian'}
    return render_template('index.html', title='Home page', user=user)


@app.route('/login')
def login():
    return render_template('login.html', title='Sign In')

