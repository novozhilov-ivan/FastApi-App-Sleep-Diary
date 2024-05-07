from api.routes import ns_auth
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.token import AccessTokenInfo

response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_auth,
    model=AccessTokenInfo,
)

from api.routes.auth.refresh.refresh import AuthRefreshJWTRoute  # noqa

refresh_endpoint = "refresh"
ns_auth.add_resource(
    AuthRefreshJWTRoute,
    f"/{refresh_endpoint}",
    endpoint=refresh_endpoint,
)
