from flask import Blueprint
from flask_restx import Api

from src.application.api.namespaces.main import namespace_main


# from src.application import auth


def init_api_blueprint() -> Blueprint:
    api_blueprint = Blueprint("sleep_diary_api", __name__)
    api = Api(
        app=api_blueprint,
        # prefix="/api",
        doc="/doc",
        ordered=True,
        validate=True,
        default_mediatype="application/json",
        # authorizations=auth.authorizations,
        # security=[
        #     auth.bearer,
        #     auth.oauth2,
        # ],
    )

    api.add_namespace(namespace_main)
    return api_blueprint
