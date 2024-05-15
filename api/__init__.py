from flask import Flask

from api.config import config
from api.extension import api, db


# TODO add ruff[isort, etc] | linters | pre-commit


def create_app() -> Flask:
    # Initialize Flask App
    app = Flask(
        import_name="api",
        instance_relative_config=False,
    )
    app.config.from_object(config)

    # Initialize Plugins
    db.init_app(app)
    api.init_app(
        app=app,
        title="API для дневника сна",
        description="Описание дневника сна",
    )

    # Create DataBase Tables
    with app.app_context():
        from api.models import Notation, User

        db.create_all()

    # Register Namespaces
    from api.routes import (
        ns_main,
        ns_sleep,
        ns_edit,
        ns_auth,
        ns_account,
    )

    api.add_namespace(ns_main)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_account)
    api.add_namespace(ns_sleep)
    api.add_namespace(ns_edit)
    return app
