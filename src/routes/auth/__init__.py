from flask_restx import Namespace

from src.exceptions.handlers import handler_unprocessable_entity_422

ns_auth: Namespace = Namespace(
    name="Authentication",
    description="Аутентификация, авторизация, регистрация, выпуск access и refresh "
    "токенов, а также удаление токенов авторизации.",
    path="/",
    decorators=[],
)
ns_auth.errorhandler(handler_unprocessable_entity_422)
