from flask import send_from_directory
from flask_restx import Resource

from api.routes.main import main_page_response_model_200, ns_main


class MainRoute(Resource):
    @ns_main.response(**main_page_response_model_200)
    def get(self):
        response = send_from_directory(
            directory="static/content/",
            path="main.json"
        )
        return response
