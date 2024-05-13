from api.routes.auth import ns_auth
from api.utils.auth import response_invalid_username_or_password_401
from api.utils.payload import create_payload_from_model
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.token import TokenInfo
from common.pydantic_schemas.user import UserCredentials

response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_auth,
    model=TokenInfo,
)
response_model_401 = response_schema(
    code=HTTP.UNAUTHORIZED_401,
    ns=ns_auth,
    description=response_invalid_username_or_password_401,
)

signin_params = create_payload_from_model("form", UserCredentials)

from api.routes.auth.sign_in.sign_in import AuthUserRoute  # noqa

signin_endpoint = "signin"
ns_auth.add_resource(
    AuthUserRoute,
    f"/{signin_endpoint}",
    endpoint=signin_endpoint,
)
