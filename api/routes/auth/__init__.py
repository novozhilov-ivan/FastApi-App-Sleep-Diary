from flask_restx import Namespace

from api.exceptions.handlers import handler_unprocessable_entity_422

ns_auth = Namespace(
    name="auth",
    description="Описание auth",
    path="/",
)
ns_auth.errorhandler(handler_unprocessable_entity_422)
