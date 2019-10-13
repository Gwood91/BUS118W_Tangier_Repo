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


@app.route('/login')
def login():
    return render_template('login.html', title='Sign In')

