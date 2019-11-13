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
from __init__ import db, app


def init_db():
    with app.app_context():
        db.create_all()


<<<<<<< HEAD
class User(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # db relationships for users with recruiter privelages and their projects

    # db relationships for users and their private messages
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='messenger', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.recipient_id', backref='messengee', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


# Getting users from the database
users = User.query.all()
for u in users:
    print(u.username)


=======
>>>>>>> bca40bd03138814fdafb57f4fa5bf4dc51c74735
# The Post class are blog posts written by Users
class Post(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # timestamp Will receive posts in chronological order
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # user_id references an id value from the Users table, SQL-Alchemy automatically uses lower case characters for model names which is why user.id is a lower case u
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


# Work in progress... need to get to add to database***
# Similiar to Post Table, except 2 user foreign keys are used here. The User model gets the 
# relationship between the two users. 
class Message(db.Model):
    __table_args__ = {'extend_existing': True}
<<<<<<< HEAD
<<<<<<< HEAD
    id = db.Column(db.Integer, primary_key=True)
    # references the id value from the Users table
=======
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True, unique=True)
>>>>>>> bca40bd03138814fdafb57f4fa5bf4dc51c74735
=======
    id = db.Column(db.Integer, primary_key=True)
>>>>>>> parent of bca40bd... Begin User Profile
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


# create an association table for talent pools and projects
talent_pool_table = db.Table('talent_pool',
                             db.Column('project_id', db.Integer, db.ForeignKey('recruiter__project.id')),  # use double underscore if needed
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                             extend_existing=True
                             )


class Recruiter_Project(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(96))
    description = db.Column(db.String(256))
    # talent_pool = db.relationship(
        # "recruiter_project", secondary=talent_pool_table,
        #primaryjoin=(talent_pool_table.c.project_id == id),
        #secondaryjoin=(talent_pool_table.c.project_id == id),
        # backref=db.backref("talent_pool_table", lazy='dynamic'), lazy='dynamic')
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
        db.session.delete(self)


"""TO DO: RELATIONSHIP DOES NOT WORK"""


class User_Profile(db.Model):
    # __tablename__ = "user_profile"
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.String(120), index=True, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    profile_picture = db.Column(db.String(64))
    #user = relationship("User", back_populates="user_profile")
    user_bio = db.Column(db.String(256))
    skills = db.Column(db.String(256))
    experience = db.Column(db.String(256))


# user_recruiter_project_table = db.Table('user_recruiter_project',
                                        # db.Column('project_id', db.Integer, db.ForeignKey('Recruiter_Project.id')),  # use double underscore if needed
                                        #db.Column('owner_id', db.Integer, db.ForeignKey('user.id')),
                                        # extend_existing=True
                                        # )


class User(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    first_name = db.Column(db.String(24))
    last_name = db.Column(db.String(24))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    #project = db.relationship('Recruiter_Project', backref='author', lazy='dynamic')
    """TO DO: RELATIONSHIP DOES NOT WORK"""
    #user_profile = relationship("User_Profile", uselist=False, back_populates="user")
    # db relationships for users with recruiter privelages and their projects
    """TO DO: RELATIONSHIP DOES NOT WORK"""
    # recruiter_project = db.relationship(
        # "User", secondary=user_recruiter_project_table,
        #primaryjoin=(user_recruiter_project_table.c.owner_id == id),
        #secondaryjoin=(user_recruiter_project_table.c.owner_id == id),
        # backref=db.backref("user_recruiter_project", lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)



# initialize the database
init_db()
# Getting users from the database
user_query = User.query.all()
for u in user_query:
    print(u.username)

