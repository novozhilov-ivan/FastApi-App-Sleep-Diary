import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv(find_dotenv())
app = Flask(__name__, template_folder='templates', static_folder="static")
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
