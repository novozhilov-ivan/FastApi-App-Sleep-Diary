import os

from dotenv import load_dotenv

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# todo попробовать взять и задействовать from psycopg2 import connect

load_dotenv()
DATABASE_URI='postgresql://lqdyhlvwlirokb:d2aa84740d77846e6b1aa25745a2e2c7db22cba92a2b69cb815a4c9444639d60@ec2-52-30-67-143.eu-west-1.compute.amazonaws.com:5432/d2l2sup15h6ek1'

app = Flask('Sleep diary', template_folder='app/templates', static_folder='app/static')
# Для создания локальной бд
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleep_diary.db'
# Для пользования или для серверной бд
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Создание бд: from app import db; db.create_all()
db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'
login_manager.login_message = "Дневник сна доступен только авторизованным пользователям"
