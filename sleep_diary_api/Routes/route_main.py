from flask import send_from_directory
from flask_restx import Resource, Namespace

main_page_info = Namespace('api')


@main_page_info.route("/")
@main_page_info.route("/main")
class MainPageInfo(Resource):
    def get(self):
        response = send_from_directory(
            directory="static/content/",
            path="main.json"
        )
        return response
