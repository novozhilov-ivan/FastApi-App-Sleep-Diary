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
#           DDD
#   - подумать над дефолт значениями у entity: назначать в orm или в domain?
#   - подучать над типами данных в oid и в user.password
#   - tests/.../test_orm.py < Протестировать orm.py
#   -
#   - .../repo/fake.py удалить и переместить класс в tests_repo.py
#   - src/.../services.py < Добавить службу сервисного слоя write(
#   note, repo, session).
#   - services.py < Добавить ошибки, службы для проверки, etc.
#   - tests/.../test_services.py < Добавить тесты служб сервисов
#   - Diary + Week взаимодействие
#   - Diary < метод make_diary() для формирования словаря/json с записями
#   разделенными неделями, со своими сортировками

# TODO
#   etc. Добавить абстрактный репозиторий, фейковый и SQLAlchemy
#    2.1 Добавить тесты репозиториев.
#    2.2 Протестировать репозиторий Sqlalchemy с sqlite::memory
#    2.3 Удалить зависимость Flask-SQLAlchemy и db.init_app(app).
#       Заменить на session = session_maker(session_options).
#       И вызов with session() as session: ...

# TODO
#   3.Добавить сервисы/сервисный слой

# TODO
#  0. Зависимости:
#   dev+ pre-committer
#   dev+ ipython
#   dev+ sqlite driver
#   prod-+ Flask-SQLAlchemy -> SQLAlchemy
# TODO
#   Рассмотреть замену flask-restx. Начать с "connexion".
#   Иначе хорошо исправить мой вспомогательный код описания параметров для
#   swagger ui, чтоб не ругал mypy и flake8

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
