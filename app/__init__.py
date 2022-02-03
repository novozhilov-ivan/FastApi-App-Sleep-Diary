import os
from flask import Flask
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
app = Flask(__name__)

# Load App Settings
app.config.from_pyfile('config.py')

from .views import *
# from .models import *

# # If production mode
# if (os.getenv('FLASK_ENV')) == "production":
#     pass
