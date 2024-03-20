from flask import Flask
from flask_login import LoginManager

from .extension import api, db
from .config import Config


# flask -e sleep_diary_api/.env -A sleep_diary_api run -h 0.0.0.0 -p 8080 --reload

def create_app():
    app = Flask(
        'sleep_diary_api',
        static_folder='static'
    )
    app.config.from_object(Config)

    # Initialize Plugins
    db.init_app(app)
    with app.app_context():
        from . import Routes

        api.init_app(app, title="API для дневника сна")
        api.add_namespace(Routes.ns_main)
        api.add_namespace(Routes.ns_sleep)

        # Create Database Models
        db.create_all()
        return app

# login_manager = LoginManager(app)
# login_manager.login_view = 'sign_in'
# login_manager.login_message = "Дневник сна доступен только авторизованным пользователям"
#
# from app import Routes, exceptions
