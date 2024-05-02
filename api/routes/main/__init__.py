from flask_restx import Namespace

from api.schemas.flask_api_models import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.main import MainPageModel

ns_main = Namespace(
    name="main",
    description="Описание main page",
    path="/",
)

response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_main,
    model=MainPageModel,
)

from api.routes.main.route_main import MainRoute  # noqa

main_endpoint = "main"
ns_main.add_resource(MainRoute, "/", "/main", endpoint=main_endpoint)
