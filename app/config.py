import os
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleepdairy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

APP_MODE = os.getenv('FLASK_ENV')
