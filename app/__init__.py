import os
from flask import Flask
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
app = Flask(__name__)

# Load App Settings
app.config.from_pyfile('config.py')

# Views необходимо импортировать после app = Flask(__name__), иначе ошибка из-за зациклености наследования
from .views import *

# Смысл нахождения этой хуйни - если мы не в production, то можем читать данный файл(как?)
# If production mode
if (os.getenv('FLASK_ENV')) == "production":
    pass
