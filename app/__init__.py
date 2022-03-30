# Load App Settings
from app.config import app
from app.view import *

app.config.from_pyfile('config.py')
