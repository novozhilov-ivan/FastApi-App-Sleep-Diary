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
#   - Создать ErrorSchema - схема для ответа http
#   при возникновении Error из domain и services_layer
#   - определить общий интерфейс Base Error/Exception для создания
#   других ошибок. поправить имеющиеся схемы
#   -
#   - Добавить тест /note_add
#   -
#   - IDiaryRepository < разделить метод get и другие на _get и get:
#   def get(...) -> "" будет постоянным, т.е. определен в абстрактном классе;
#   def _get(...) будет интерфейсом, имплементируемый в субклассе;
#   -
#   - Протестировать каскадное удаление записей при удалении user.
#   - (all, delete-orphan) в таблице 'users' мб нужно выставить.
#   -
#   -
#   - (Зачем? мб провалидировать строки сразу.
#   - В каком слое размещать эти переменные?)
#   - Добавить pydantic валидацию переменных bedtime_date, oid и временных точек,
#   для валидации данных и конвертации типа данных;
#   services_test < поправить тесты  после создания.
#   - Добавить валидацию аргументов службы предметной области и мб служб
#   сервисного слоя
#   -
#   - Diary + Week взаимодействие
#   Diary < метод make_diary() для формирования словаря/json с записями
#   разделенными неделями, со своими сортировками
#   -
#   -
#   - Удалить зависимость Flask-SQLAlchemy и db.init_app(app).
#   Заменить на session = session_maker(session_options).
#   И вызов with session() as session: ...


# TODO
#  0. Зависимости:
#   dev+ pre-committer
#   dev+ ipython
#   prod-+ Flask-SQLAlchemy -> SQLAlchemy

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
