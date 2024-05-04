from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

http_bearer = "Bearer"
auth_bearer = {
    "HTTPBearer": {
        "type": "apiKey",
        "in": "header",
        "name": "Bearer Token Authentication",
    }
}


class Base(DeclarativeBase):
    pass


api = Api(
    prefix="/api",
    doc="/doc",
    ordered=True,
    validate=True,
    default_mediatype="application/json",
    authorizations=auth_bearer,
    security=[],
)
db = SQLAlchemy(model_class=Base)
