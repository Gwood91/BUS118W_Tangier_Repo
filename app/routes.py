# import sys modules
import sys
import os
# define the path for the current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
# change the directory to the venv on the machine of the current user
os.chdir(local_path)
print(os.getcwd())
# import modules
from flask import Flask, g, render_template, redirect, url_for, session, request, flash
# these two modules are for the candidate checker
# install this mkl for gensim error
#from gensim.summarization.summarizer import summarize
from fuzzywuzzy.fuzz import ratio
from app import app

"""THE FOLLOWING CODE IS DEPRECATED"""
# change the directory to current user
#current_user = user_root = os.path.expanduser('~')
#local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
# sys.path.append(local_path)
#from app import app
"""END DEPRECATION"""


# define the routes


@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/profile')
def profile():
    return render_template('profile.html', title='Profile', i=5)


@app.route('/message')
def message():
    return render_template('message.html', title='Direct Messaging')


@app.route('/jobs')
def jobs():
    return render_template('jobs.html', title='Jobs')


@app.route('/myNetwork')
def my_network():
    return render_template('myNetwork.html', title='myNetwork')


# for recruitment clients
@app.route('/recruiter', methods=['GET', 'POST'])
def recruiter_page():
    if request.method == 'GET':
        return render_template('recruiter_page.html', title='Recruiter', candidate_analysis="NULL", i=15)
    # if the recruiter client is evaluating the potential match of a candidate
    if request.method == 'POST':
        # get the input element with a given name from the posted from
        candidate_text = str(request.form.get("candidateText", None))
        search_criteria = str(request.form.get("searchCriteria", None))
        # analysing the natural language of the profile text
        #candidate_summary = summarize(candidate_text)
        candidate_match = ratio(candidate_text, search_criteria)
        #summary_match = ratio(candidate_summary, search_criteria)
        current_cand_analysis = "Candidate Match: " + str(candidate_match)
        #current_cand_analysis = "Candidate Match: " + str(candidate_match) + "%\n" + "Summary Match: " + str(summary_match) + "%"
        return render_template('recruiter_page.html', title='Recruiter', candidate_analysis=current_cand_analysis, i=5)


@app.route('/candidate_search', methods=['GET', 'POST'])
def candidate_search():
    if request.method == 'GET':
        return render_template('recruiter_candidate_search.html', title='Candidate Search', i=5)
    # if the recruiter client is evaluating the potential match of a candidate
    if request.method == 'POST':
        # get the data supplied by the client and construct sanitzed queries in the db
        candidate_text = str(request.form.get("candidateText", None))
        search_criteria = str(request.form.get("searchCriteria", None))


@app.route('/newProject', methods=['GET', 'POST'])
def create_project():
    if request.method == 'GET':
        return render_template('recruiter_create_project.html', title='Create Project', i=5)
    # if the recruiter client is evaluating the potential match of a candidate
    if request.method == 'POST':
        # get the data supplied by the client and construct sanitzed queries in the db
        project_title = str(request.form.get("projectTitle", None))
        project_description = str(request.form.get("projectDescription", None))
        return str(project_title + project_description + """<a href=" / recruiter" style="float: right"><button>Return to Recruiter View</button></a>""")
