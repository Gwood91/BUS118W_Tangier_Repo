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

