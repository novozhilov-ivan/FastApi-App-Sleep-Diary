from flask import Flask

from src.config import (
    flask_config,
    flask_restx_config,
    flask_sqlalchemy_config,
)
from src.extension import Base, api, db, engine


# TODO add ruff[isort, etc] | linters mypy | pre-commit.

# TODO Рефакторинг архитектуры под DDD.
#  1. Отделить бизнес логику в domain и Протестировать
#   1.1 NoteBase, NoteFieldsValidators, NoteValueObject, NoteStatistics, NoteEntity
#   1.2 WeekBase, WeekFieldsValidators, WeekValueObject, WeekStatistics, WeekEntity
#    или убрать прослойку Week и сделать это computed_field в Diary
#   1.3 DiaryBase, DiaryStatistics, etc
#  2. Добавить Базовый репозиторий, фейковый и SQLAlchemy
#  3.Добавить сервисы/сервисный слой

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
    from src import routes

    api.add_namespace(routes.ns_main)
    api.add_namespace(routes.ns_auth)
    api.add_namespace(routes.ns_account)
    api.add_namespace(routes.ns_notes)
    api.add_namespace(routes.ns_diary)
    api.add_namespace(routes.ns_edit)

    return app
