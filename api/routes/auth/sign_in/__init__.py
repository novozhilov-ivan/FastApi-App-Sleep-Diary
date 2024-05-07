from api.routes.auth import ns_auth
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

signin_params = create_payload_from_model("form", UserCredentials)

from api.routes.auth.sign_in.login import AuthUserAndCreateJWTRoute  # noqa

signin_endpoint = "signin"
ns_auth.add_resource(
    AuthUserAndCreateJWTRoute,
    f"/{signin_endpoint}",
    endpoint=signin_endpoint,
)
