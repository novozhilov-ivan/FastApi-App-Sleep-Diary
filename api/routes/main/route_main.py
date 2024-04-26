from flask import Response
from flask_restx import Resource

from api.routes.main import main_page_response_model_200, ns_main
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.main import MainPageModel


class MainRoute(Resource):
    @ns_main.doc(description='Главная страница с описанием приложения')
    @ns_main.response(**main_page_response_model_200)
    def get(self):
        response = MainPageModel().model_dump_json()
        return Response(response, HTTP.OK_200, content_type='application/json')
