from flask import render_template

import sys
sys.path.append('/Users/gwood/Tangier')
from app import app 

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Christian'}
    return render_template('index.html', title='Home page', user=user)

@app.route('/login')
def login():
    return render_template('login.html', title='Sign In')

@app.route('/profile')
def profile():
    return render_template('profile.html', title='Profile Page')

@app.route('/network')
def network():
    return render_template('network.html', title='Network Page')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html', title='Jobs!')

@app.route('/message')
def message():
    return render_template('message.html', title='Send a message')