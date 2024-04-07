from flask_restx import Namespace

from api.schemas.flask_api_models import response_schema

from common.pydantic_schemas.main import MainPageModel


ns_main = Namespace(
    name='main',
    description='Описание main page',
    path='/',
    validate=True
)

main_page_response_model_200 = response_schema(
    code=200,
    ns=ns_main,
    model=MainPageModel,
)

from api.routes.main.route_main import MainRoute
ns_main.add_resource(MainRoute, '/', '/main')
