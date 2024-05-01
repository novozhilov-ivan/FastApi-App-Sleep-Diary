from api.routes.auth import ns_auth
from api.schemas.flask_api_models import response_schema
from api.schemas.payload import create_payload_from_model
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserLogIn

response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_auth,
    model=UserLogIn,
)
login_params = create_payload_from_model("json", UserLogIn)

from api.routes.auth.login.login import LogInRoute  # noqa

ns_auth.add_resource(LogInRoute, "/login")
