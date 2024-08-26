from flask import Blueprint
from flask_restx import Api

from src.application import authentication
from src.application.api.namespaces.main import namespace_main
from src.application.api.namespaces.notes.namespace import namespace_notes


def init_api_blueprint() -> Blueprint:
    api_blueprint = Blueprint("api", __name__)
    api = Api(
        app=api_blueprint,
        doc="/doc",
        ordered=True,
        validate=True,
        default_mediatype="application/json",
        authorizations=authentication.authorizations,
        security=[
            authentication.bearer,
            authentication.oauth2,
        ],
    )
    api.add_namespace(namespace_main)
    api.add_namespace(namespace_notes)
    return api_blueprint
