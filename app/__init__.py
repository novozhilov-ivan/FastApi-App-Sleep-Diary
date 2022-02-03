# import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())
app = Flask(__name__)
db = SQLAlchemy(app)

from app import models
from app import views



# # Load App Settings
# app.config.from_pyfile('config.py')
#
# # If production mode
# if (os.getenv('FLASK_ENV')) == "production":
#     pass
