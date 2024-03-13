from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from sleep_diary_api.extension import api, db
from sleep_diary_api.config import Config
from sleep_diary_api.Routes import main_page_info


# flask -e .env -A app run -h 0.0.0.0 -p 8080 --reload

def create_app():
    app = Flask(
        'sleep_diary_api',
        static_folder='static'
    )

    app.config.from_object(Config)
    api.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    api.add_namespace(
        main_page_info
    )
    return app

# login_manager = LoginManager(app)
# login_manager.login_view = 'sign_in'
# login_manager.login_message = "Дневник сна доступен только авторизованным пользователям"
#
# from app import Routes, exceptions
