# import modules
import os
import sys
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

current_user = os.path.expanduser('~')
local_engine_path = "sqlite:////" + current_user
engine = create_engine(local_engine_path)


app = Flask(__name__)

app.config.from_object(Config)



# Flask-SQLAlchemy initialization
# db object represents the database
db = SQLAlchemy(app)

# For migration purposes if needed 
# change the directory to current user
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
sys.path.append(local_path)


# models module defines the structure of the database
from app import routes, models
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)

