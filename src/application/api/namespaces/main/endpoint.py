from http import HTTPStatus

from flask_restx import Resource

from src.application.api.namespaces.main.schemas import MainEndpointSchema


class MainEndpoint(Resource):
    NAME: str = "main"

    @staticmethod
    def get() -> tuple[dict, HTTPStatus]:
        return MainEndpointSchema().model_dump(), HTTPStatus.OK
