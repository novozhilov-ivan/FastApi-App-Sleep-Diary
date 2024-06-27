from flask_restx.reqparse import RequestParser

from src.pydantic_schemas.token import TokenInfo
from src.pydantic_schemas.user import UserCredentials
from src.routes.auth import ns_auth
from src.utils.auth import response_invalid_username_or_password_401
from src.utils.payload import create_payload_from_model
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP

response_model_200: dict = response_schema(
    code=HTTP.OK_200,
    ns=ns_auth,
    model=TokenInfo,
)
response_model_401: dict = response_schema(
    code=HTTP.UNAUTHORIZED_401,
    ns=ns_auth,
    description=response_invalid_username_or_password_401,
)

signin_params: RequestParser = create_payload_from_model(
    location="form",
    model=UserCredentials,
)

from src.routes.auth.sign_in.sign_in import AuthUserRoute  # noqa

signin_endpoint = "signin"
ns_auth.add_resource(
    AuthUserRoute,
    f"/{signin_endpoint}",
    endpoint=signin_endpoint,
)
