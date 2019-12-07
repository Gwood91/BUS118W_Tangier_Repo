# import sys modules
import sys
import os
import base64
from datetime import datetime
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
from flask_wtf import FlaskForm
from sqlalchemy import or_
# may need to update plotly/ pip install ipywidgets
import plotly.graph_objs as go
import plotly
import json
from itertools import groupby
from tangie import fetch_headlines, generate_dashboard_vis, filter_content
"""TODO: Probably gonna need to change the double directory change here, need to consolidate"""
# change the directory to current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
sys.path.append(local_path)
"""an important distinction here is that we are importing the db module, not the db object created in __init__"""
from app import app, db
from models import User, User_Profile, Recruiter_Project, Message, Post, Project_Candidate, Job_Post, Job_Applicant, Likes


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


@app.route('/home', methods=['GET', 'Post'])
def home():
    if g.user is not None:
        current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    else:
        current_user = None
    # fetch the headlines
    news_stories = fetch_headlines()
    if request.method == "GET":
        return render_template('home.html', title='Home', news_stories=news_stories, current_user=current_user, db=db, User=User, User_Profile=User_Profile, str=str, len=len, list=list)
    if request.method == 'POST':
        status_body = str(request.form.get("statusBody", None))
        """filter status body for profanity using SVM"""
        status_body = filter_content(status_body)
        # create new post object
        status_post = Post(user_id=current_user.id, body=status_body, poster_fname=current_user.first_name, poster_lname=current_user.last_name)
        # commit new user post to db
        db.session.add(status_post)
        db.session.commit()
        return redirect(url_for('home'))


@app.route('/home/login', methods=['GET'])
@oidc.require_login
def login_handler():
    return redirect(url_for('home'))


@app.route('/logout', methods=['Post'])
def logout_handler():
    oidc.logout()
    return redirect(url_for('home'))


@app.route('/feed/like/<post_id>', methods=['GET'])
@oidc.require_login
def like(post_id):
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    current_post = db.session.query(Likes).filter_by(post_id=post_id).first()
    liked_post = Likes(post_id=post_id, user_id=current_user.id)
    exists = db.session.query(Likes).filter_by(user_id=current_user.id, post_id=post_id).first()
    # determine if like exists already for current user and current post
    if exists is None:
        # create like object and cast to db
        db.session.add(liked_post)
        db.session.commit()
    if exists is not None:
        # unlike status post
        db.session.delete(current_post)
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
@oidc.require_login
def profile():
    connections = 5  # this is just a dummy value until a network connections query link is established
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    exists = db.session.query(User_Profile.user_id).filter_by(user_id=current_user.id).scalar()
    if exists is None:
        u = User_Profile(id=current_user.id, user_id=current_user.id, profile_picture="", user_bio="", skills="", experience="")
        db.session.add(u)
        db.session.commit()
    profile = db.session.query(User_Profile).filter_by(id=current_user.id).first()
    if request.method == "GET":
        return render_template('profile.html', title='Profile', connections=5, current_user=current_user)
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
            return render_template('profile.html', title='Profile', connections=5, profile=profile, profile_img=profile.profile_picture, current_user=current_user)
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
        return render_template('profile.html', title='Profile', connections=5, profile=profile, profile_img=profile.profile_picture, current_user=current_user)


@app.route('/messagePage', methods=['GET', 'POST'])
@oidc.require_login
def messagePage():
    # Users = User.query.all()
        get_users = User.query.all()
        news_feed = ['message', 'message', 'message', 'message', 'message', 'message', 'message', 'message', 'message']
        user = db.session.query(User).filter_by(email=g.user.profile.email).first_or_404()

        if request.method == 'GET':
            return render_template('messagePage.html', title='Direct Messaging', user=user, news_feed=news_feed, get_users=get_users)
        if request.method == 'POST':
            # get the data supplied by the client and construct sanitzed queries in the db
            recipient_id = str(request.form.get("selectAUser", None))
            print(recipient_id, file=sys.stderr)
            message_body = str(request.form.get("sendaDM", None))
            # user = User.query.filter_by(username=Message.recipient_id).first_or_404()
            # user = db.session.query(User).filter_by(username=recipient_id).first()
            recipient_first_name, recipient_last_name = recipient_id.split(" ")
            recipient_user = db.session.query(User).filter_by(first_name=recipient_first_name, last_name=recipient_last_name).first_or_404()
            new_message = Message(sender_id=user.id, recipient_id=recipient_user.id, body=message_body, unread=True, sender_fname=user.first_name, sender_lname=user.last_name)
            db.session.add(new_message)
            db.session.commit()
            # flash(_('Your message has been sent!'))

            return render_template('messagePage.html', title='Direct Messaging', user=user, news_feed=news_feed, get_users=get_users)


@app.route('/jobs', methods=['GET', 'POST'])
@oidc.require_login
def jobs():
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    if request.method == 'GET':
        jobs = db.session.query(Job_Post).all()
        return render_template('jobs.html', title='Jobs', current_user=current_user, jobs=jobs, len=len)
    if request.method == 'POST':
        city = str(request.form.get("city", None))
        state = str(request.form.get("state", None))
        job_title = str(request.form.get("jobTitle", None))
        keywords = str(request.form.get("keywords", None))
        skills = str(request.form.get("skills", None))
        query = [city, state, job_title, keywords, skills]
        formatted_query = []
        # format each string for SQL like operation
        for item in query:
            if item is not None:
                formatted_query.append(item)
                item = (str("%{}%".format(item)))

        # unpack the list
        city, state, job_title, keywords, skills = tuple(formatted_query)
        # execute client query
        jobs = db.session.query(Job_Post).\
            filter(Job_Post.city.contains(city), Job_Post.state.contains(state), Job_Post.description.contains(skills), Job_Post.title.contains(job_title), Job_Post.description.contains(keywords),).all()
        return render_template('jobs.html', title='Jobs', current_user=current_user, jobs=jobs, len=len)


@app.route('/jobs/view/<job_id>', methods=['GET', 'POST'])
@oidc.require_login
def view_job(job_id):
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    current_job = db.session.query(Job_Post).filter_by(id=job_id).first_or_404()
    if request.method == 'GET':
        jobs = db.session.query(Job_Post).all()
        return render_template('view_job.html', title=current_job.title, current_user=current_user, current_job=current_job)
    if request.method == 'POST':
        city = str(request.form.get("city", None))
        return render_template('view_job.html', title=current_job.title, current_user=current_user, current_job=current_job)


@app.route('/jobs/apply/<job_id>', methods=['GET', 'POST'])
@oidc.require_login
def job_apply(job_id):
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    exists = db.session.query(Job_Applicant).filter_by(user_id=current_user.id, job_post_id=job_id).first()
    # make sure users can only to apply once to any given job
    if exists is None:
        new_applicant = Job_Applicant(job_post_id=job_id, user_id=current_user.id)
        db.session.add(new_applicant)
        db.session.commit()
    return redirect(url_for('jobs'))


@app.route('/myNetwork', methods=['GET', 'POST'])
@oidc.require_login
def my_network():
    query_profiles = []
    if request.method == 'GET':
        return render_template('myNetwork.html', title='myNetwork', query_profiles=query_profiles)
    if request.method == 'POST':
        # the query group returned resulting from the user search
        search = str(request.form.get("search", None))
        search = "%{}%".format(search)
        query_profiles = db.session.query(User_Profile).\
            filter(or_(User_Profile.user_bio.contains(search), User_Profile.skills.contains(search), User_Profile.experience.contains(search))).all()
        query_users = db.session.query(User).\
            filter(or_(User.first_name.contains(search), User.last_name.contains(search))).all()
        for profile in query_profiles:
            user = db.session.query(User).filter_by(id=profile.user_id).first()
            if user not in query_users:
                query_users.append(user)
        results_count = len(query_users)
        return render_template('myNetwork.html', title='myNetwork', query_users=query_users, db=db, User=User, results_count=results_count)


@app.route('/user-profile/<username>', methods=['GET', 'POST'])
@oidc.require_login
def view_user(username):
    client_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    current_user = db.session.query(User).filter_by(username=username).first()
    title = current_user.first_name + " " + current_user.last_name
    if request.method == 'GET':
        return render_template('view_user_profile.html', title=title, current_user=current_user, client_user=client_user)
    if request.method == 'POST':
        return redirect(url_for('follow', username=current_user.username))


@app.route('/follow/<username>')
@oidc.require_login
def follow(username):
    client_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    client_user.follow(user)
    user.follow(client_user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('view_user', username=username))


@app.route('/unfollow/<username>')
@oidc.require_login
def unfollow(username):
    client_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    client_user.unfollow(user)
    user.unfollow(client_user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('view_user', username=username))

# for recruitment clients


@app.route('/recruiter', methods=['GET', 'POST'])
@oidc.require_login
def recruiter_page():
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    if request.method == 'GET':
        user_projects = db.session.query(Recruiter_Project).filter_by(user_id=current_user.id).all()
        candidate_pool = []
        candidate_dataset = []
        # get the candidates from each recruiter project a
        for project in user_projects:
            for candidate in project.candidates:
                candidate_dataset.append(candidate)  # dataset for data science
                candidate_pool.append(db.session.query(User).filter_by(id=candidate.user_id).first())  # retrieve user objects for canidates
        """HERE IS A SOMEWHAT PRIMATIVE METHOD OF GENERATING DASHBOARD VISUALS"""  # TODO: REFINE
        timestamp_data = []
        cand_count_data = [0]
        """Need to fix the dates and get a count by datetime to the hour"""
        for candidate in candidate_dataset:
            format_time = str(candidate.timestamp).split(" ")[0]
            timestamp_data.append(format_time)
        time_count = 0
        for time in timestamp_data:
            if time == format_time:
                time_count += 1
        # get canidate count by datetime
        cand_count_data = [0] + [len(list(group)) for key, group in groupby(timestamp_data)]
        # cand_count_data.append(time_count)
        timestamp_data = ["Dawn of Time"] + timestamp_data
        timestamp_unique = []
        for time_stamp in timestamp_data:
                # check if exists in unique_list or not
                if time_stamp not in timestamp_unique:
                    timestamp_unique.append(time_stamp)
        plt.style.use('dark_background')  # change the color theme
        fig, ax = plt.subplots()
        ax.set_title("Daily Recruiting Activity")  # set the axis title
        # ax.plot(timestamp_data, cand_count_data)  # create the plot
        ax.fill_between(timestamp_unique, cand_count_data)
        print(cand_count_data, timestamp_unique, file=sys.stderr)
        ax.grid("on")
        img = plt.savefig("plt_img", format='png')  # save the plot as base64 string
        with open("plt_img", "rb") as img_file:
            raw_base64 = str(base64.b64encode(img_file.read()))
            plt_a_base64 = "src=" + "data:image/png;base64,{}"
            plt_a_base64 = plt_a_base64.format(raw_base64[2:-1])  # format the base 64 string for html rendering
        # get the candidates from each recruiter project a
        """GAUGE CHART/RADIAL GAUGE"""
        radial_plot = go.Figure(go.Indicator(
            domain={'x': [0, 1], 'y': [0, 1]},
            value=cand_count_data[-1],
            mode="gauge+number+delta",
            title={'text': "Recruiter Activity"},
            delta={'reference': 0},
            gauge={'axis': {'range': [None, 15]},
                   'steps': [
                {'range': [0, 3], 'color': "lightgray"},
                {'range': [5, 10], 'color': "gray"}],
                'threshold': {'line': {'color': "blue", 'width': 4}, 'thickness': 0.75, 'value': 25}}))
        radial_plot.write_image("plt_img_b.png")
        with open("plt_img_b.png", "rb") as img_file:
            raw_base64 = str(base64.b64encode(img_file.read()))
            plt_b_base64 = "src=" + "data:image/png;base64,{}"
            plt_b_base64 = plt_b_base64.format(raw_base64[2:-1])
        applicant_list = []
        job_posts = db.session.query(Job_Post).filter_by(profile_id=current_user.profile.id).all()
        for post in job_posts:
            for applicant in post.applicants:
                applicant_list.append(applicant)
        plt_c = generate_dashboard_vis(applicant_list, title="Applicant Activity")
        return render_template('recruiter_page.html', title='Recruiter', candidate_analysis="NULL", i=15, plt_a=plt_a_base64, plt_b=plt_b_base64, plt_c=plt_c, current_user=current_user, candidate_pool=candidate_pool)
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
        return render_template('recruiter_page.html', title='Recruiter', current_user=current_user, candidate_analysis=current_cand_analysis, candidate_pool=candidate_pool)


@app.route('/recruiter/view/<project_id>', methods=['GET', 'POST'])  # view/edit a given project
@oidc.require_login
def view_project(project_id):
    project = db.session.query(Recruiter_Project).filter_by(id=project_id).first_or_404()
    candidate_pool = []
    # fetch the user objects for profiles in search query
    for candidate in project.candidates:
        candidate_pool.append(db.session.query(User).filter_by(id=candidate.user_id).first())
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
    candidates = db.session.query(Project_Candidate).filter_by(project_id=project_id).first_or_404()
    db.session.delete(candidates)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for('recruiter_page'))


@app.route('/candidate_search', methods=['GET', 'POST'])
@oidc.require_login
def candidate_search():
    i = 5
    query_results = []
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    user_projects = db.session.query(Recruiter_Project).filter_by(user_id=current_user.id).all()
    results_len = len(query_results)
    if request.method == 'GET':
        return render_template('recruiter_candidate_search.html', title='Candidate Search', results=query_results, results_len=results_len, i=5, current_user=current_user)
    # if the recruiter client is evaluating the potential match of a candidate
    if request.method == 'POST':
        # get the data supplied by the client and construct sanitzed queries in the db
        major = str(request.form.get("major", None))
        industry = str(request.form.get("industry", None))
        keywords = str(request.form.get("keywords", None))
        skills = str(request.form.get("skills", None))
        project_name = str(request.form.get("projectName", None))
        keywords_search = "%{}%".format(keywords)
        skill_search = "%{}%".format(skills)
        # if field is not blank
        if skills != "" or keywords != "":
            # or filter based on user input
            if keywords != "" and skills != "":
                query_profiles = db.session.query(User_Profile).\
                    filter(or_(User_Profile.user_bio.contains(keywords_search), User_Profile.experience.contains(keywords_search), User_Profile.skills.contains(keywords_search))).all()
            elif skills != "":
                query_profiles = db.session.query(User_Profile).filter(User_Profile.skills.contains(skill_search)).all()
            elif keywords != "":
                query_profiles = db.session.query(User_Profile).filter(User_Profile.experience.contains(keywords)).all()
            query_results = []
            # fetch the user objects for profiles in search query
            if query_profiles is not None:
                for profile in query_profiles:
                    query_results.append(db.session.query(User).filter_by(id=profile.id).first())
            results_len = len(query_results)
        return render_template('recruiter_candidate_search.html', title='Candidate Search', results=query_results, results_len=results_len, current_user=current_user, i=i)


@app.route('/view_candiate/<username>', methods=['GET', 'POST'])
@oidc.require_login
def view_candidate(username):
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    current_candiate = db.session.query(User).filter_by(username=username).first()
    candidate_fullname = current_candiate.first_name + " " + current_candiate.last_name
    if request.method == 'GET':
        return render_template('candidate_profile.html', title=candidate_fullname, current_candiate=current_candiate, current_user=current_user)
    if request.method == 'POST':
        project_name = str(request.form.get("projectName", None))
        project_id = db.session.query(Recruiter_Project).filter_by(title=project_name, user_id=current_user.id).first().id
        return redirect(url_for('add_candidate', username=username, project_id=project_id))


@app.route('/recruiter/<project_id>/add/<username>', methods=['GET'])
@oidc.require_login
def add_candidate(username, project_id):
    if request.method == 'GET':
        candidate = db.session.query(User).filter_by(username=username).first()
        project_canidate = Project_Candidate(user_id=candidate.id, project_id=project_id)
        # add user to project
        if project_id is not None:
            db.session.add(project_canidate)
            db.session.commit()
        return redirect(url_for('recruiter_page'))


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
        new_project = Recruiter_Project(profile_id=user.profile.id, user_id=user.id, description=project_description, title=project_title)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('recruiter_page'))


@app.route('/newJob', methods=['GET', 'POST'])
@oidc.require_login
def create_job():
    if request.method == 'GET':
        return render_template('recruiter_create_job_post.html', title='Create Job Post', i=5)
    # if the recruiter client is evaluating the potential match of a candidate
    if request.method == 'POST':
        # get the data supplied by the client and construct sanitzed queries in the db
        job_title = str(request.form.get("jobTitle", None))
        company = str(request.form.get("company", None))
        industry = str(request.form.get("industry", None))
        job_type = str(request.form.get("jobType", None))
        salary = str(request.form.get("salary", None))
        city = str(request.form.get("city", None))
        state = str(request.form.get("state", None))
        job_description = str(request.form.get("jobDesc", None))
        experience_level = str(request.form.get("experienceLevel", None))
        user = db.session.query(User).filter_by(email=g.user.profile.email).first()
        new_job = Job_Post(title=job_title, company=company, description=job_description, experience_level=experience_level, industry=industry, job_type=job_type, salary=salary, city=city, state=state, profile_id=user.profile.id)
        db.session.add(new_job)
        db.session.commit()
        return redirect(url_for('recruiter_page'))


@app.route('/recruiter/job/<job_post_id>', methods=['GET', 'POST'])  # view/edit a given project
@oidc.require_login
def view_edit_job(job_post_id):
    # check if the current user is authorized to access the project
    current_user = db.session.query(User).filter_by(email=g.user.profile.email).first()
    job_post = db.session.query(Job_Post).filter_by(id=job_post_id, profile_id=current_user.profile.id).first_or_404()
    applicants = []
    # fetch the user objects for profiles in search query
    for applicant in job_post.applicants:
        applicants.append(db.session.query(User).filter_by(id=applicant.user_id).first())
    if request.method == 'GET':
        return render_template('recruiter_view_edit_job_post.html', title=job_post.title, job_post=job_post, applicants=applicants)
    if request.method == 'POST':
        job_title = str(request.form.get("jobTitle", None))
        company = str(request.form.get("company", None))
        industry = str(request.form.get("industry", None))
        job_type = str(request.form.get("jobType", None))
        salary = str(request.form.get("salary", None))
        city = str(request.form.get("city", None))
        state = str(request.form.get("state", None))
        job_description = str(request.form.get("jobDesc", None))
        experience_level = str(request.form.get("experienceLevel", None))

        job_post.title = job_title
        job_post.company = company
        job_post.industry = industry
        job_post.job_type = job_type
        job_post.salary = salary
        job_post.city = city
        job_post.state = state
        job_post.description = job_description
        job_post.experience_level = experience_level
        # update the the db session to save the above changes
        db.session.commit()
        return render_template('recruiter_view_edit_job_post.html', title=job_post.title, job_post=job_post, applicants=applicants)
