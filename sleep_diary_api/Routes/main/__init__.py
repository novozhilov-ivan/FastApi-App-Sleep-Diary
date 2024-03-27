from flask_restx import Namespace

from sleep_diary_api.Api_schemas.flask_api_models import response_schema
from sleep_diary_api.Routes import general_path_prefix

from src.pydantic_schemas.main_info import MainPageModel


ns_main = Namespace(
    name='main',
    description='Описание main page',
    path=general_path_prefix,
    validate=True
)

main_page_response_model_200 = response_schema(
    200,
    'Информация на главной странице.',
    ns_main,
    MainPageModel
)

from sleep_diary_api.Routes.main.route_main import MainRoute
ns_main.add_resource(MainRoute, '/main', '/')
