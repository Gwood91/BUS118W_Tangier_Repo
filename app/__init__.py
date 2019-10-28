# import modules
import os
import sys
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config.from_object(Config)

# Flask-SQLAlchemy and Flask-Migrate initialization
# db object represents the database
db = SQLAlchemy(app)
# For migration purposes if needed 
migrate = Migrate(app, db)
# change the directory to current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
sys.path.append(local_path)




# models module defines the structure of the database
from app import routes, models
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)

