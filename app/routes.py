# import modules
import sys
from flask import render_template
import os
# change the directory to current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
sys.path.append(local_path)
from app import app

# define the routes


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



