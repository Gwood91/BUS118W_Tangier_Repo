# import modules
import sys
from flask import Flask, g, render_template, redirect, url_for, session, request, flash
import os
# these two modules are for the candidate checker
from gensim.summarization.summarizer import summarize
from fuzzywuzzy.fuzz import ratio

# change the directory to current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
sys.path.append(local_path)
from app import app


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
        candidate_summary = summarize(candidate_text)
        candidate_match = ratio(candidate_text, search_criteria)
        summary_match = ratio(candidate_summary, search_criteria)
        current_cand_analysis = "Candidate Match: " + str(candidate_match) + "%\n" + "Summary Match: " + str(summary_match) + "%"
        return render_template('recruiter_page.html', title='Recruiter', candidate_analysis=current_cand_analysis, i=5)

