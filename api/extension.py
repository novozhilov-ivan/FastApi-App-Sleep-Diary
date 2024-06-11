from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from api.config import sqlalchemy_config


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(
    model_class=Base,
    session_options=sqlalchemy_config.session_options,
    engine_options=sqlalchemy_config.engine_options,
    disable_autonaming=True,
)
engine = create_engine(**sqlalchemy_config.engine_options)

bearer = "Bearer"
oauth2 = "oauth2"
authorizations = {
    bearer: {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": (
            "Enter the token with the `Bearer` prefix, e.g. 'Bearer abcde12345'"
        ),
    },
    oauth2: {
        "type": "oauth2",
        "flow": "password",
        "tokenUrl": "api/signin",
        "authorizationUrl": "api/signin",
    },
}

api = Api(
    prefix="/api",
    doc="/doc",
    ordered=True,
    validate=True,
    default_mediatype="application/json",
    authorizations=authorizations,
    security=[
        bearer,
        oauth2,
    ],
)
