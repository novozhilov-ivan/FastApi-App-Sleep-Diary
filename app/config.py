import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(
    'Sleep diary',
    template_folder='app/templates',
    static_folder='app/static'
)
DB_DRIVER = os.getenv('DB_DRIVER')
DB_EXTEND_DRIVER = os.getenv('DB_EXTEND_DRIVER')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = "{}+{}://{}:{}@{}:{}/{}".format(
app.config['SQLALCHEMY_DATABASE_URI'] = "{}://{}:{}@{}:{}/{}".format(
    DB_DRIVER,
    # DB_EXTEND_DRIVER,
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_PORT,
    DB_NAME,
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_ECHO'] = True if os.getenv('SQLALCHEMY_ECHO') == 'True' else None
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
mode = True if os.getenv('FLASK_ENV') == 'development' else False

db = SQLAlchemy(app)

# Необходимо для создания базы данных и/или таблиц в ней
# from app.model import Notation, User
# from app.config import db

db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'
login_manager.login_message = "Дневник сна доступен только авторизованным пользователям"
