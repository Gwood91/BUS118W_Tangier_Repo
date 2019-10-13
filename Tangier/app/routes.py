
import sys
sys.path.append('/Users/gwood/Tangier')
from app import app 
@app.route('/')
@app.route('/index')
def index():
    return 'It has fucking begun!!!!!!!!!'
