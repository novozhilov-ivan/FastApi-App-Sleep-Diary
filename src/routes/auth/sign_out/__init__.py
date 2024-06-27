from src.routes.auth import ns_auth
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP

response_ok_200 = "User is sign out"
response_model_200: dict = response_schema(
    code=HTTP.OK_200,
    ns=ns_auth,
    description=response_ok_200,
)

from src.routes.auth.sign_out.sign_out import DeAuthUserRoute  # noqa

signout_endpoint = "signout"
ns_auth.add_resource(
    DeAuthUserRoute,
    f"/{signout_endpoint}",
    endpoint=signout_endpoint,
)
