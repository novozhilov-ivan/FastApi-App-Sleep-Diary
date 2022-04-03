import os

from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()


app = Flask('Sleep diary', template_folder='app/templates', static_folder='app/static')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}" \
                                        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_ECHO'] = True if os.getenv('SQLALCHEMY_ECHO') == 'True' else None

db = SQLAlchemy(app)

# Необходимо для создания базы данных
# from app.model import Notation, User
# db.create_all()


login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'
login_manager.login_message = "Дневник сна доступен только авторизованным пользователям"
