# import sys modules
import sys
import os
import base64
# define the path for the current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/app/"
# change the directory to the venv on the machine of the current user
os.chdir(local_path)
print(os.getcwd())
# import modules
from flask import Flask, g, render_template, redirect, url_for, session, request, flash
# these two modules are for the candidate checker
# install this mkl for gensim error
# from gensim.summarization.summarizer import summarize
from fuzzywuzzy.fuzz import ratio
# modules for okta authentication
import oidc
from flask_oidc import OpenIDConnect
from okta import UsersClient
from oauth2client.client import OAuth2Credentials
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import StringIO
"""TODO: Probably gonna need to change the double directory change here, need to consolidate"""
# change the directory to current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
sys.path.append(local_path)
from app import app, db
from models import User, User_Profile, Recruiter_Project, Project_Candidate, Message, Post


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

# preload request


@app.before_request
def before_request():
    """ Load a proper user object using the user ID from the ID token. This way, the
     `g.user` object can be used at any point"""
    if oidc.user_loggedin:
        g.user = okta_client.get_user(oidc.user_getfield("sub"))
        user = db.session.query(User).filter_by(email=g.user.profile.email).first()
        # handle newly registered users who are not in our db
        if user == None:
            new_user = User(first_name=g.user.profile.firstName, last_name=g.user.profile.lastName, username=g.user.profile.email, email=g.user.profile.email)
            # append user to db
            db.session.add(new_user)
            db.session.commit()
        user_client = user

    else:
        g.user = None
# define the routes


@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html', title='Home')


@app.route('/home', methods=['Post'])
@oidc.require_login
def login_handler():
    return render_template('home.html', title='Home')


@app.route('/profile', methods=['GET', 'POST'])
@oidc.require_login
def profile():
    connections = 5  # this is just a dummy value until a network connections query link is established
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    exists = db.session.query(User_Profile.user_id).filter_by(user_id=current_user.id).scalar()
    if exists is None:
        u = User_Profile(user_id=current_user.id, profile_picture="", user_profile="", skills="", experience="")
        db.session.add(u)
        db.session.commit()
    profile = db.session.query(User_Profile).filter_by(id=current_user.id).first()
    if request.method == "GET":
        return render_template('profile.html', title='Profile', connections=5, profile=profile, profile_img=profile.profile_picture)
    # update profile page
    if request.method == 'POST':
        if 'Save_Profile' in request.form:
            user_bio = str(request.form.get("user_bio", None))
            skills = str(request.form.get("skills", None))
            experience = str(request.form.get("experience", None))
            # save get data and save changes to db
            profile.user_bio = user_bio
            profile.skills = skills
            profile.experience = experience
            db.session.commit()
            return render_template('profile.html', title='Profile', connections=5, profile=profile, profile_img=profile.profile_picture)
        elif 'save_img' in request.form:
           # gather the image from the file upload
            try:
                image = request.files['Upload_Image']
                # convert uploaded image to base64 and strip the detritus
                profile_img = str(base64.b64encode(image.read()))
                profile_img = profile_img.split("'")[1]
                # with open(profile_img, "rb") as image_file:
                   # profile_img = base64.b64encode(image_file.read())
                profile.profile_picture = profile_img
                db.session.commit()
                print('image upload error', image)
            except:
                print('no file chosen')
            return render_template('profile.html', title='Profile', connections=5, profile=profile, profile_img=profile.profile_picture)


@app.route('/messagePage', methods=['GET', 'POST'])
def messagePage():
    return render_template('messagePage.html', title='Direct Messaging')


@app.route('/jobs')
def jobs():
    return render_template('jobs.html', title='Jobs')


@app.route('/myNetwork')
@oidc.require_login
def my_network():
    # the query group returned resulting from the user search
    """temporary variable condition"""
    query_listing = 5
    return render_template('myNetwork.html', title='myNetwork', query_listing=query_listing)


# for recruitment clients
@app.route('/recruiter', methods=['GET', 'POST'])
@oidc.require_login
def recruiter_page():
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    user_projects = db.session.query(Recruiter_Project).filter_by(user_id=current_user.id)
    if request.method == 'GET':
        """HERE IS A SOMEWHAT PRIMATIVE METHOD OF GENERATING DASHBOARD VISUALS"""  # TODO: REFINE
        x = [1, 5, 6, 8, 9]  # sample x values, these will be derived from some query into the db
        y = [12, 16, 11, 17, 22]  # sample y values, these will be derived from some query into the db
        plt.style.use('dark_background')  # change the color theme
        fig, ax = plt.subplots()
        ax.set_title("Recruiter Activity")  # set the axis title
        ax.plot(x, y)  # create the plot
        ax.grid("on")
        img = plt.savefig("plt_img", format='png')  # save the plot as base64 string
        with open("plt_img", "rb") as img_file:
            raw_base64 = str(base64.b64encode(img_file.read()))
            plt_a_base64 = "src=" + "data:image/png;base64,{}"
            plt_a_base64 = plt_a_base64.format(raw_base64[2:-1])  # format the base 64 string for html rendering
        """TODO: USE PLOTLY FOR THE GAUGE CHART/RADIAL GAUGE"""
        return render_template('recruiter_page.html', title='Recruiter', candidate_analysis="NULL", i=15, plt_a=plt_a_base64, projects=user_projects, current_user=current_user)
    # if the recruiter client is evaluating the potential match of a candidate
    if request.method == 'POST':
        # get the input element with a given name from the posted from
        candidate_text = str(request.form.get("candidateText", None))
        search_criteria = str(request.form.get("searchCriteria", None))
        # analysing the natural language of the profile text
        # candidate_summary = summarize(candidate_text)
        candidate_match = ratio(candidate_text, search_criteria)
        # summary_match = ratio(candidate_summary, search_criteria)
        current_cand_analysis = "Candidate Match: " + str(candidate_match)
        # current_cand_analysis = "Candidate Match: " + str(candidate_match) + "%\n" + "Summary Match: " + str(summary_match) + "%"
        return render_template('recruiter_page.html', title='Recruiter', candidate_analysis=current_cand_analysis, i=5, current_user=current_user)


@app.route('/recruiter/view/<project_id>', methods=['GET', 'POST'])  # view/edit a given project
@oidc.require_login
def view_project(project_id):
    project = db.session.query(Recruiter_Project).filter_by(id=project_id).first_or_404()
    candidate_pool = db.session.query(Project_Candidate).filter_by(project_id=project.id).all()
    if request.method == 'GET':
        return render_template('recruiter_view_edit_project.html', title=project.title, project=project, candidate_pool=candidate_pool)
    if request.method == 'POST':
        # get the data supplied by the client and construct sanitzed queries in the db
        project_title = str(request.form.get("projectTitle", None))
        project_description = str(request.form.get("projectDescription", None))
        # edit the db fields for the project to reflect saved user changes
        project.title = project_title
        project.description = project_description
        # update the the db session to save the above changes
        db.session.commit()
        return render_template('recruiter_view_edit_project.html', title=project.title, project=project, candidate_pool=candidate_pool)


# if user decides to remove project


@app.route('/recruiter/remove/<project_id>')
@oidc.require_login
def remove_project(project_id):
    project = db.session.query(Recruiter_Project).filter_by(id=project_id).first_or_404()
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('recruiter_page'))


@app.route('/candidate_search', methods=['GET', 'POST'])
@oidc.require_login
def candidate_search():
    query_results = []
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    user_projects = db.session.query(Recruiter_Project).filter_by(user_id=current_user.id).all()
    results_len = len(query_results)
    if request.method == 'GET':
        return render_template('recruiter_candidate_search.html', title='Candidate Search', results=query_results, results_len=results_len, i=5, user_projects=user_projects)
    # if the recruiter client is evaluating the potential match of a candidate
    if request.method == 'POST':
        # get the data supplied by the client and construct sanitzed queries in the db
        major = str(request.form.get("major", None))
        industry = str(request.form.get("industry", None))
        keywords = str(request.form.get("keywords", None))
        skills = str(request.form.get("skills", None))
        projectName = str(request.form.get("projectName", None))
        skill_search = "%{}%".format(skills)
        keyword_search = "%{}%".format(keywords)
        if skills or keywords != "":
            # multi part query, default without and_ method comma separated list of conditions are AND
            query_results = db.session.query(User_Profile).\
                filter(User_Profile.skills.contains(skill_search), User_Profile.user_bio.contains(keyword_search)).all()

        results_len = len(query_results)
        return render_template('recruiter_candidate_search.html', title='Candidate Search', results=query_results, results_len=results_len, i=5, user_projects=user_projects)


@app.route('/newProject', methods=['GET', 'POST'])
@oidc.require_login
def create_project():
    if request.method == 'GET':
        return render_template('recruiter_create_project.html', title='Create Project', i=5)
    # if the recruiter client is evaluating the potential match of a candidate
    if request.method == 'POST':
        # get the data supplied by the client and construct sanitzed queries in the db
        project_title = str(request.form.get("projectTitle", None))
        project_description = str(request.form.get("projectDescription", None))
        user = db.session.query(User).filter_by(email=g.user.profile.email).first()
        new_project = Recruiter_Project(user_id=user.id, description=project_description, title=project_title)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('recruiter_page'))
