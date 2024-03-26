from flask import send_from_directory
from flask_restx import Resource, Namespace

from src.pydantic_schemas.main_info import MainPage

ns_main = Namespace('api')

main_page_response_model = ns_main.schema_model(
    'Main page info schema',
    MainPage.model_json_schema()
)


@ns_main.route("/", "/main")
@ns_main.response(
    code=200,
    description='Информация на главной странице.',
    model=main_page_response_model
)
class MainInfo(Resource):
    def get(self):
        response = send_from_directory(
            directory="static/content/",
            path="main.json"
        )
        return response
