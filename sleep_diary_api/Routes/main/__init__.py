from flask_restx import Namespace

from sleep_diary_api.Api_schemas.flask_api_models import response_schema
from sleep_diary_api.Routes import api_prefix

from src.pydantic_schemas.main_info import MainPageModel


ns_main = Namespace(
    name='main',
    description='Описание main page',
    path=api_prefix,
    validate=True
)

main_page_response_model_200 = response_schema(
    code=200,
    ns=ns_main,
    model=MainPageModel,
    description='Информация на главной странице.',
)

from sleep_diary_api.Routes.main.route_main import MainRoute
ns_main.add_resource(MainRoute, '/main', '/')
