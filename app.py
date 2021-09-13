import os
from flask import Flask
from src.controller.index import index_page
from src.controller.error import error_page

# load app
app = Flask(__name__, template_folder='src/view')
app.debug = True

# Load blueprints
app.register_blueprint(index_page)
app.register_blueprint(error_page)

# create tmp directory for upload 
os.makedirs(os.path.dirname(app.instance_path) + '/tmp', exist_ok=True)

# upload configs
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.vtt']
app.config['UPLOAD_PATH'] = os.path.dirname(app.instance_path) + '/tmp'
