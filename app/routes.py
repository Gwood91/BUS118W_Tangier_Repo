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
    return render_template('index.html', title='Home')


@app.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')

@app.route('/message')
def message():
    return render_template('message.html', title='Direct Messaging')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html', title='Jobs')

@app.route('/myNetwork')
def myNetwork():
    return render_template('myNetwork.html', title='Jobs')



