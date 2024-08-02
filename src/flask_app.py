from flask import Flask

from src import routes
from src.config import (
    flask_config,
    flask_restx_config,
    flask_sqlalchemy_config,
)
from src.extension import (
    Base,
    api,
    db,
    engine,
)


# TODO
#  0. Зависимости:
#   dev+ pre-committer
#   dev+ ipython
#   dev+ sqlite driver
#   prod-+ Flask-SQLAlchemy -> SQLAlchemy

# TODO
#  Рефакторинг архитектуры под DDD в пунктах 1 и 2.

# TODO
#    1.3 DiaryStatistics, etc Diary.
#       Diary нужен для возврата json с данными, а также
#       он должен иметь @classmethod для создания Diary из множества с Note.

# TODO
#   2. Добавить абстрактный репозиторий, фейковый и SQLAlchemy
#    2.1 Добавить тесты репозиториев.
#    2.2 Протестировать репозиторий Sqlalchemy с sqlite::memory
#    2.3 Удалить зависимость Flask-SQLAlchemy и db.init_app(app).
#       Заменить на session = session_maker(session_options).
#       И вызов with session() as session: ...

# TODO
#   3.Добавить сервисы/сервисный слой
#    3.1 Рассмотреть замену flask-restx. Начать с "connexion".
#      Иначе хорошо исправить мой вспомогательный код описания параметров для
#      swagger ui, чтоб не ругал mypy и flake8

# TODO
#   4. CI/CD


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
