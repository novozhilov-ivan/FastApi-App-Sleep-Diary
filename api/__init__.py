from flask import Flask

from api.config import flask_config, flask_restx_config, sqlalchemy_config
from api.extension import Base, api, db, engine
from api.models import SleepNoteOrm, UserOrm


# TODO add ruff[isort, etc] | linters | pre-commit
# TODO добавить файл example.env для файлов с необходимыми переменными окружениями


def create_app() -> Flask:
    # Initialize Flask App
    app = Flask(
        import_name="api",
        instance_relative_config=False,
    )
    app.config.from_object(flask_config)
    app.config.from_object(flask_restx_config)
    # Initialize Plugins
    db.init_app(
        app=app,
    )
    api.init_app(
        app=app,
        title="API для дневника сна",
        description="Описание дневника сна",
    )

    # Create DataBase Tables
    Base.metadata.create_all(
        bind=engine,
    )

    # Register Namespaces
    from api.routes import (
        ns_main,
        ns_diary,
        ns_edit,
        ns_auth,
        ns_account,
        ns_notes,
    )

    api.add_namespace(ns_main)
    api.add_namespace(ns_auth)
    api.add_namespace(ns_account)
    api.add_namespace(ns_notes)
    api.add_namespace(ns_diary)
    api.add_namespace(ns_edit)

    return app
