# User database model/schema
import base64
import os
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()
# from sqlalchemy import db
# define the path for the current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/app/"
# change the directory to the venv on the machine of the current user
os.chdir(local_path)
"""an import and noteworthy distinction here is that we are importing a module named app not an object such as declared in __init__"""
from app import db, app


def init_db():
    with app.app_context():
        db.create_all()
# likes for status posts


class Likes(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


# The Post class are status posts written by Users
class Post(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # timestamp Will receive posts in chronological order
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # user_id references an id value from the Users table, SQL-Alchemy automatically uses lower case characters for model names which is why user.id is a lower case u
    # This is going to be the ID of the user who authors the post**
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = relationship("Likes")
    poster_fname = db.Column(db.String(96))
    poster_lname = db.Column(db.String(96))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# Work in progress... need to get to add to database***
# Similiar to Post Table, except 2 user foreign keys are used here. The User model gets the
# relationship between the two users.
class Message(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True, unique=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    unread = db.Column(db.Boolean, default=True, nullable=True)
    sender_fname = db.Column(db.String(96))
    sender_lname = db.Column(db.String(96))

    def __repr__(self):
        return '<Message {}>'.format(self.body)

    def inbox_count(self):
        db.session.query(Message).filter_by(id=id, unread=True)


class Recruiter_Project(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    profile_id = db.Column(db.Integer, db.ForeignKey('user__profile.id'))
    title = db.Column(db.String(96))
    description = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    candidates = relationship("Project_Candidate")

    def is_talent(self, user):
        return self.candidates.filter(
            candidates.c.user_id == user.id).count() > 0

    def add_talent(self, user):
        # validate logic and connect users
        if self.is_talent(user) == False:  # if user not already in talent pool
            self.talent_pool.append(user)

    def remove_talent(self, user):
        # validate logic and connect users
        if self.is_talent(user) == False:  # if user not already in talent pool
            self.talent_pool.remove(user)

    def create(self):
        # remove self from recruiter projects table
        db.session.add(self)

    def delete(self):
        # remove self from recruiter projects table
        db.session.delete(self)


class Project_Candidate(db.Model):
    __tablename__ = 'Project_Candidate'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column('project_id', db.Integer, db.ForeignKey('recruiter__project.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Job_Applicant(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    job_post_id = db.Column('job_post_id', db.Integer, db.ForeignKey('job__post.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)


class Job_Post(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    company = db.Column(db.String(140))
    description = db.Column(db.String())
    experience_level = db.Column(db.Integer())
    industry = db.Column(db.String(140))
    job_type = db.Column(db.String(140))
    salary = db.Column(db.Integer())
    city = db.Column(db.String(140))
    state = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    profile_id = db.Column(db.Integer, db.ForeignKey('user__profile.id'))
    applicants = relationship("Job_Applicant")


class User_Profile(db.Model):
    # __tablename__ = "user_profile"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(120), index=True, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    profile_picture = db.Column(db.String(128))
    user_bio = db.Column(db.String(256))
    skills = db.Column(db.String(256))
    experience = db.Column(db.String(256))
    recruiter_projects = relationship('Recruiter_Project', backref='user_profile', lazy=True)
    job_posts = relationship("Job_Post", backref="user_profile")


followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(24))
    last_name = db.Column(db.String(24))
    email = db.Column(db.String(120), index=True, unique=True)
    profile = relationship("User_Profile", uselist=False, backref="User")
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='author', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id', backref='recipient', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id).order_by(
            Post.timestamp.desc())


# initialize the database
init_db()
# Getting users from the database
user_query = User.query.all()
for u in user_query:
    print(u.username)

