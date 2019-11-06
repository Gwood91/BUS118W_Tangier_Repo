# User database model/schema
import base64
import os
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
# from sqlalchemy import db
# define the path for the current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/app/"
# change the directory to the venv on the machine of the current user
os.chdir(local_path)
from __init__ import db, app


def init_db():
    with app.app_context():
        db.create_all()


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # db relationships for users with recruiter privelages and their projects

    def __repr__(self):
        return '<User {}>'.format(self.username)


# Getting users from the database
users = User.query.all()
for u in users:
    print(u.username)


# The Post class are blog posts written by Users
class Post(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # timestamp Will receive posts in chronological order
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # user_id references an id value from the Users table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# Getting posts from the database
posts = Post.query.all()
for p in posts:
    print(p.body)


# Work in progress... need to get to add to database***
class Message(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)



# create an association table for talent pools and projects
talent_pool_table = db.Table('talent_pool',
                             db.Column('project_id', db.Integer, db.ForeignKey('recruiter__project.id')),  # use double underscore if needed
                             db.Column('user_id', db.Integer, db.ForeignKey('ser.id')),
                             extend_existing=True
                             )


class Recruiter_Project(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(256))
    talent_pool = db.relationship(
        "Recruiter_Project", secondary=talent_pool_table,
        primaryjoin=(talent_pool_table.c.project_id == id),
        secondaryjoin=(talent_pool_table.c.project_id == id),
        backref=db.backref("talent_pool_table", lazy='dynamic'), lazy='dynamic')
    # determine if a given user is included within the talent pool

    def is_talent(self, user):
        return self.talent_pool.filter(
            talent_pool_table.c.user_id == user.id).count() > 0

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
        db.session.remove(self)


init_db()
