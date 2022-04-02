import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask('Sleep diary', template_folder='app/templates', static_folder='app/static')

# Для создания локальной бд
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sleep_diary.db'
# Для пользования или для серверной бд
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@" \
                                        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Создание бд: from app import db; db.create_all()
db = SQLAlchemy(app)


login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'
login_manager.login_message = "Дневник сна доступен только авторизованным пользователям"
