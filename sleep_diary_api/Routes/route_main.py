from flask import send_from_directory
from flask_restx import Resource, Namespace

from sleep_diary_api.extension import api
from src.pydantic_schemas.main_info import MainPageInfoSchema

main_page = Namespace('api')

model_main_page_response = api.schema_model(
    'Main page info schema',
    MainPageInfoSchema.model_json_schema()
)


@main_page.route("/", "/main")
@main_page.response(code=200, description='Информация на главной странице.', model=model_main_page_response)
class MainPageInfo(Resource):
    def get(self):
        response = send_from_directory(
            directory="static/content/",
            path="main.json"
        )
        return response
