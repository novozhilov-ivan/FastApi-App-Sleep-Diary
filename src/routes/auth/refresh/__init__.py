from src.pydantic_schemas.token import AccessTokenInfo
from src.routes import ns_auth
from src.utils.jwt import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    response_invalid_token_type_401,
)
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP

response_model_200: dict = response_schema(
    code=HTTP.OK_200,
    ns=ns_auth,
    model=AccessTokenInfo,
)
response_model_401: dict = response_schema(
    code=HTTP.UNAUTHORIZED_401,
    ns=ns_auth,
    description=response_invalid_token_type_401.format(
        f"{ACCESS_TOKEN_TYPE!r}",
        f"{REFRESH_TOKEN_TYPE!r}",
    ),
)

from src.routes.auth.refresh.refresh import AuthRefreshJWTRoute  # noqa

refresh_endpoint = "refresh"
ns_auth.add_resource(
    AuthRefreshJWTRoute,
    f"/{refresh_endpoint}",
    endpoint=refresh_endpoint,
)
