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
#   - Инфраструктура framework'а Flask и интеграция Flask-RestX с низкой
#   связанностью:
#   - Прочитать доку/src Flask + Flask_RestX;
#   - Посмотреть репозитории, в которых используют Flask;
#   для создания endpoint'ов через декоратор, класс Resource и через Blueprint.
#   а также получение url для Blueprint'ов через url_for();
#   - Отделить создание flask endpoint'ов от регистрации их в flask-restx
#   namespace'ах???
#   - Пофиксить переопределение endpoint'ов в namespace, когда делаем
#   ns.add_resource;
#   -
#   - Сервис авторизации:
#   -Переписать;
#   -UserRepo;
#   -Схемы User'а;
#   -Как использовать с application?;
#   -Реализация sign-out, через хранилище в cache и RedisCache;
#   -Создание в памяти public и private keys для шифрования при тестировании;
#   -
#   - Тест /note_add Определить форму ответа:
#   - body с сообщением(каким? общая схема для всех ответов нужна.);
#   - header location '/api/notes/<uuid:43fgf...>';
#   - Тест /note_add для ошибок; Тест с параметрами;
#   -
#   - IDiaryRepository < переименовать в Notes; разбить мб на Base... и I... :
#   - методы private сделать шаблонными; а одноименные public их будут вызывать и
#   сводить к единому типу;
#   -
#   - IDiaryRepository < разделить метод get и другие на _get и get:
#   def get(...) -> "" будет постоянным, т.е. определен в абстрактном классе;
#   def _get(...) будет интерфейсом, имплементируемый в субклассе;
#   -
#   - BaseDatabase и тесты для FakeDatabase.
#   - Установить Аннотацию типа у session в Database. Сейчас pycharm не понимает.
#   -
#   - Протестировать каскадное удаление записей при удалении user.
#   - (all, delete-orphan) в таблице 'users' мб нужно выставить.
#   -
#   - Mypy error: str | time в NoteValueObject
#   -
#   - (мб провалидировать строки сразу. Зачем?
#   - В каком слое размещать эти переменные?)
#   - Добавить pydantic валидацию переменных bedtime_date, oid и временных точек,
#   для валидации данных и конвертации типа данных;
#   services_test < поправить тесты  после создания.
#   - Добавить валидацию аргументов службы предметной области и мб служб
#   сервисного слоя
#   -
#   - Добавить зависимость для реализации Dependency Injection Container.
#   - Заменить вызовы переиспользуемых объектов.
#   -
#   - Diary + Week взаимодействие
#   Diary < метод make_diary() для формирования словаря/json с записями
#   разделенными неделями, со своими сортировками


# TODO
#  Зависимости:
#   dev+ pre-committer
#   dev+ ipython

# TODO
#   CI/CD


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
