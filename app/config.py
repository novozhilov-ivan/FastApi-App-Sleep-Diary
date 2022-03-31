import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


app = Flask('project-sleep-diary', template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sleep_diary_postgresql.db'
# Если создавать вручную локальную бд, то как сверху код
# Если по грамотному держать все важное в переменном окружении то как снизу
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
APP_MODE = os.getenv('FLASK_ENV')
load_dotenv(find_dotenv())


# Создание бд: from app import db; db.create_all()
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'
login_manager.login_message = "Дневник сна доступен только авторизованным пользователям"
