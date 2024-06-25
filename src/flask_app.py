from flask import Flask

from src.config import (
    flask_config,
    flask_restx_config,
    flask_sqlalchemy_config,
)
from src.extension import Base, api, db, engine


# TODO add ruff[isort, etc] | linters mypy | pre-commit.

# TODO Рефакторинг архитектуры под DDD.
#  1. Отделить бизнес логику в модель предметной области - domain
#  2. Протестировать бизнес логику
#  3. Добавить Базовый репозиторий, фейковый и SQLAlchemy
#  4.Добавить сервисы/сервисный слой

# TODO Удалить зависимость Flask-SQLAlchemy и db.init_app(app).
#  Заменить на session = session_maker(session_options).
#  И вызов with session() as session: ...


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
    from src.routes import (
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
