from flask import Flask
from flask_login import LoginManager

from .extension import api, db
from .config import configuration


# flask -e sleep_diary_api/.dev.env -A sleep_diary_api run -h 0.0.0.0 -p 8080 --reload


def create_app():
    app = Flask(
        import_name="sleep_diary_api",
        instance_relative_config=False
    )

    app.config.from_object(configuration)

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        from .Routes.route_main import ns_main
        from .Routes.route_sleep import ns_sleep

        api.init_app(app, title="API для дневника сна")
        api.add_namespace(ns_main)
        api.add_namespace(ns_sleep)

        # Create Database Models
        db.create_all()
        return app


# login_manager = LoginManager(app)
# login_manager.login_view = 'sign_in'
# login_manager.login_message = "Дневник сна доступен только авторизованным пользователям"
#
# from app import Routes, exceptions
