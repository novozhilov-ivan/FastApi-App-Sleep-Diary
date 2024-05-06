from flask_restx import Namespace

from api.exceptions.handlers import handler_unprocessable_entity_422
from api.utils.auth import (
    response_invalid_authorization_token_401,
    validate_auth_token,
)
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserInfo

ns_account = Namespace(
    name="account",
    description="Описание account",
    path="/",
    decorators=[
        validate_auth_token,
    ],
)

response_model_200 = response_schema(
    ns=ns_account,
    model=UserInfo,
    code=HTTP.OK_200,
)
response_model_401 = response_schema(
    ns=ns_account,
    description=response_invalid_authorization_token_401,
    code=HTTP.UNAUTHORIZED_401,
)

ns_account.errorhandler(handler_unprocessable_entity_422)

from api.routes.account.account import UserAccountRoute  # noqa

account_endpoint = "account"
ns_account.add_resource(
    UserAccountRoute,
    "/account",
    endpoint=account_endpoint,
)
