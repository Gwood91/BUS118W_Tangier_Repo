# import modules
import os
import sys
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
# define the local path
current_user = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
local_engine_path = "sqlite:////" + local_path + 'app/app.db'
engine = create_engine(local_engine_path)


app = Flask(__name__)

app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = local_engine_path

# getting the css framework
bootstrap = Bootstrap(app)
# db object represents the database
db = SQLAlchemy(app)
# create the migration obect
migrate = Migrate(app, db)

# # change the directory to current user
# local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
# sys.path.append(local_path)


# models module defines the structure of the database
import routes
import models
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)

