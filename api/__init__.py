from flask import Flask

from api.extension import api, db, login_manager
from api.config import config


def create_app() -> Flask:
    # Initialize flask app
    app = Flask(import_name="api", instance_relative_config=False)
    app.config.from_object(config)

    # Initialize Plugins
    db.init_app(app)
    api.init_app(
        app=app,
        title="API для дневника сна",
        description='Описание дневника сна'
    )
    # login_manager.init_app(app)

    # Create Database models
    with app.app_context():
        db.create_all()

    # Register Namespaces
    from api.routes import ns_main, ns_sleep, ns_edit
    api.add_namespace(ns_main)
    api.add_namespace(ns_sleep)
    api.add_namespace(ns_edit)

    return app
