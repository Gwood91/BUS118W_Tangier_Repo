# import the modules
import os
import sys

# change the directory to current user
current_user = user_root = os.path.expanduser('~')
local_path = current_user + "/Documents/GitHub/BUS118W_Tangier_Repo/"
sys.path.append(local_path)
# import the flask application
from app import app
if __name__ == "__main__":
    app.debug = True
    app.run(port=5000)
