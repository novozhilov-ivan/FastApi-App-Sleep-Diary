from flask_restx import Namespace, Resource

from api.exceptions.handlers import handler_unprocessable_entity_422
from api.utils.jwt import (
    response_invalid_authorization_token_401,
    validate_auth_token,
)
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP

ns_account = Namespace(
    name="User account info",
    description="Информация об аккаунте пользователя",
    path="/account",
    decorators=[
        validate_auth_token,
    ],
)

response_model_401 = response_schema(
    ns=ns_account,
    description=response_invalid_authorization_token_401,
    code=HTTP.UNAUTHORIZED_401,
)

ns_account.errorhandler(handler_unprocessable_entity_422)

from api.routes.account.account_find.account import FindAccount  # noqa
from api.routes.account.account_delete.account_delete import DeleteAccount  # noqa


# TODO Наследуются/перемешиваются схемы ответа
class AccountRoute(
    Resource,
    FindAccount,
    DeleteAccount,
): ...  # noqa


account_endpoint = "account"
ns_account.add_resource(
    AccountRoute,
    "",
    endpoint=account_endpoint,
)
