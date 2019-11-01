# import modules
import os
import sys
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

current_user = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
local_engine_path = "sqlite:////" + local_path + 'app/app.db'
engine = create_engine(local_engine_path)


app = Flask(__name__)

app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = local_engine_path

# db object represents the database
db = SQLAlchemy(app)

# change the directory to current user
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
sys.path.append(local_path)