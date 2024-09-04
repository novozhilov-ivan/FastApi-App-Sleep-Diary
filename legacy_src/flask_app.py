from legacy_src.extension import (
    Base,
    api,
    db,
    engine,
)

from flask import Flask

from src import routes
from src.config import (
    flask_config,
    flask_restx_config,
    flask_sqlalchemy_config,
)


def create_app() -> Flask:
    # Initialize Flask App
    app = Flask(import_name="sleep_diary_app")
    app.config.from_object(obj=flask_config)
    app.config.from_object(obj=flask_restx_config)
    app.config.from_object(obj=flask_sqlalchemy_config)
    # Initialize Plugins
    db.init_app(app=app)
    api.init_app(
        app=app,
        title="API для дневника сна",
        description="Описание дневника сна",
    )

    # Create DataBase Tables
    Base.metadata.create_all(bind=engine)

    # Register Namespaces
    api.add_namespace(routes.ns_main)
    api.add_namespace(routes.ns_auth)
    api.add_namespace(routes.ns_account)
    api.add_namespace(routes.ns_notes)
    api.add_namespace(routes.ns_diary)
    api.add_namespace(routes.ns_edit)

    return app
