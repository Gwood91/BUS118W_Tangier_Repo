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
# modules for okta authentication
import oidc
from flask_oidc import OpenIDConnect
from okta import UsersClient
from oauth2client.client import OAuth2Credentials

"""THE FOLLOWING CODE IS DEPRECATED"""
# change the directory to current user
#current_user = user_root = os.path.expanduser('~')
#local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
# sys.path.append(local_path)
#from app import app
"""END DEPRECATION"""
# preload request


# @app.before_request
# def before_request():
    # """ Load a proper user object using the user ID from the ID token. This way, the
     # `g.user` object can be used at any point"""
    # if oidc.user_loggedin:
        #g.user = okta_client.get_user(oidc.user_getfield("sub"))
        #user = db.session.query(User_Profile).filter_by(email=g.user.profile.email).first_or_404()
        #user_client = user
    # else:
        #g.user = None


# note: the return variable cannot have the same name as the function that is returning it
# tangier OKTA Login
app.config["DEBUG"] = True
app.config["OIDC_CLIENT_SECRETS"] = "client_secrets.json"
app.config["OIDC_COOKIE_SECURE"] = False
app.config["OIDC_CALLBACK_ROUTE"] = "/oidc/callback"
app.config["OIDC_SCOPES"] = ["openid", "email", "profile"]
app.config["SECRET_KEY"] = "kadsddhakDabjdshdsadabjkdhjkh2jh3jk395llabife395wlan7dfs9isdf83"
app.config["OIDC_ID_TOKEN_COOKIE_NAME"] = "Tangier_Token"
oidc = OpenIDConnect(app)
# argument includes Elliott's okta dev url and the Tangier Token
okta_client = UsersClient("https://dev-126675.okta.com", "00VIozFldsnyd9oqlb4ferZD507ekhVDvj3hOSxvCJ")

# define the routes


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html', title='Home')


@app.route('/home', methods=['Post'])
@oidc.require_login
def login_handler():
    return render_template('home.html', title='Home')


@app.route('/profile')
def profile():
    return render_template('profile.html', title='Profile', i=5)


@app.route('/message', methods=['GET', 'POST'])
def message():
    return render_template('message.html', title='Direct Messaging')


@app.route('/jobs')
def jobs():
    return render_template('jobs.html', title='Jobs')


@app.route('/myNetwork')
def my_network():
    # the query group returned resulting from the user search
    """temporary variable condition"""
    query_listing = 5
    return render_template('myNetwork.html', title='myNetwork', query_listing=query_listing)


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
