from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import Config


app = Flask(
    'sleep_diary',
    template_folder='app/templates',
    static_folder='app/static'
)

app.config.from_object(Config)
db = SQLAlchemy(app)

# Необходимо для создания базы данных и/или таблиц в ней
# Если указать в начале файла, то возникает ошибка циклического импорта
from app import models

db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'
login_manager.login_message = "Дневник сна доступен только авторизованным пользователям"

from app import routes, exceptions
