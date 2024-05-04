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
response_unauthorized_401 = "invalid username or password"
response_model_401 = response_schema(
    ns=ns_auth, description=response_unauthorized_401, code=HTTP.UNAUTHORIZED_401
)
login_params = create_payload_from_model("form", CreateUserCredentials)

from api.routes.auth.login.login import AuthUserIssueJWTRoute  # noqa

login_endpoint = "login"
ns_auth.add_resource(AuthUserIssueJWTRoute, "/login", endpoint=login_endpoint)
