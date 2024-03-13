import json
import os.path

from flask import send_from_directory
from flask_restx import Resource, Namespace
from flask import jsonify

main_page_info = Namespace(
    'api',
    description=None,
    path=None,
    decorators=None,
    validate=None,
    authorizations=None,
    ordered=False,
)


@main_page_info.route("/main")
class MainPageInfo(Resource):
    def get(self):
        response = send_from_directory(
            directory="static/content/",
            path="main.json"
        )
        return response
