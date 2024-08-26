from http import HTTPStatus

from flask_restx import Resource

from src.application.api.namespaces.main.schemas import MainEndPointSchema


class MainEndPoint(Resource):
    NAME: str = "main"

    @staticmethod
    def get() -> tuple[dict, HTTPStatus]:
        return MainEndPointSchema().model_dump(), HTTPStatus.OK
