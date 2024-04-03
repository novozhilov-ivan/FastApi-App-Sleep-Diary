from flask import Flask
from flask_login import LoginManager

from .extension import api, db
from .config import configuration


def create_app():
    app = Flask(
        import_name="api",
        instance_relative_config=False
    )

    app.config.from_object(configuration)

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        from .routes import ns_main
        from .routes import ns_sleep

        api.init_app(
            app,
            title="API для дневника сна",
            description='Описание дневника сна'
        )
        api.add_namespace(ns_main)
        api.add_namespace(ns_sleep)

        # Create Database models
        db.create_all()
        return app


# login_manager = LoginManager(app)
# login_manager.login_view = 'sign_in'
# login_manager.login_message = "Дневник сна доступен только авторизованным пользователям"
#
# from app import routes, exceptions
