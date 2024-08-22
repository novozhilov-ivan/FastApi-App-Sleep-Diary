from flask import Blueprint
from flask_restx import Api


# from src.entrypoints import auth


def init_api() -> Blueprint:
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

    # api.add_namespace()
    return api_blueprint
