import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleep_diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP_MODE = os.getenv('FLASK_ENV')

# Создание бд: from app import db; db.create_all()
db = SQLAlchemy(app)
MAX_CONTENT_LENGTH = 1024 * 1024
login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'
login_manager.login_message = "Дневник сна доступен только авторизованным пользователям"

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



