import os
from dotenv import load_dotenv, find_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleep_dairy.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP_MODE = os.getenv('FLASK_ENV')

# Создание бд: from app import db; db.create_all()
db = SQLAlchemy(app)
MAX_CONTENT_LENGTH = 1024 * 1024
# manager = LoginManager(app)

Errors = {
    'add': 'При добавлении записи в дневник произошла ошибка',
    'update': 'При обновлении записи в дневнике произошла ошибка',
    'value': 'Неподходящее значение',
    'syntax': 'Неподходящий формат',
    'type': 'Неподходящий тип данных',
    'database': 'При обращении к базе данных произошла ошибка',
    'file': 'Файл не был найден',
    'import': 'При импортировании произошла ошибка',
    'other': 'Прочая ошибка'
}
# Load App Settings
# app.config.from_pyfile('config.py')

# Views необходимо импортировать после app = Flask(__name__),
# иначе ошибка из-за зацикленности наследования
from app import models, views

# Смысл нахождения этой хуйни? - если мы не в production, то можем читать данный файл(как?)
# If production mode
if (os.getenv('FLASK_ENV')) == "production":
    pass
