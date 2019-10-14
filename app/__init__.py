# import modules
import os
import sys
from flask import Flask
app = Flask(__name__)

# change the directory to current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
sys.path.append(local_path)
from app import routes
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
