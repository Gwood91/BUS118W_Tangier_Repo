import os

# define the path for the current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
# change the directory to the venv on the machine of the current user
os.chdir(local_path)

# Flask-SQLAlchemy configuration 
# database location variable
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuring the database 
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False