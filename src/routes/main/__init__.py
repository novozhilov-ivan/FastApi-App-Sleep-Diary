from flask_restx import Namespace

from src.pydantic_schemas.main import MainPageModel
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP

ns_main: Namespace = Namespace(
    name="Main",
    description="Основная страница с описанием",
    path="/",
    decorators=[],
)

response_model_200: dict = response_schema(
    code=HTTP.OK_200,
    ns=ns_main,
    model=MainPageModel,
)

from src.routes.main.main import MainRoute  # noqa

main_endpoint = "main"
ns_main.add_resource(
    MainRoute,
    "/",
    "/main",
    endpoint=main_endpoint,
)
