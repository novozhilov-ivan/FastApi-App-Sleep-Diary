from api.routes.auth import ns_auth
from api.utils.payload import create_payload_from_model
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.token import TokenInfo
from common.pydantic_schemas.user import CreateUserCredentials

response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_auth,
    model=TokenInfo,
)

login_params = create_payload_from_model("form", CreateUserCredentials)

from api.routes.auth.login.login import AuthUserRoute  # noqa

login_endpoint = "login"
ns_auth.add_resource(AuthUserRoute, "/login", endpoint=login_endpoint)
