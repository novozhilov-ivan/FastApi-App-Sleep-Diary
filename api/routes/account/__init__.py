from flask_restx import Namespace

from api.exceptions.handlers import handler_unprocessable_entity_422
from api.extension import http_bearer
from api.utils.payload import create_payload
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserInfo

ns_account = Namespace(
    name="account",
    description="Описание account",
    path="/",
)
ns_account.errorhandler(handler_unprocessable_entity_422)
response_model_200 = response_schema(
    ns=ns_account,
    model=UserInfo,
    code=HTTP.OK_200,
)
headers_auth_token = create_payload(
    name="bearer_token",
    description="authentication bearer token",
    type_=http_bearer,
    location="headers",
)

from api.routes.account.account import UserAccountRoute  # noqa

account_endpoint = "account"
ns_account.add_resource(
    UserAccountRoute,
    "/account",
    endpoint=account_endpoint,
)
