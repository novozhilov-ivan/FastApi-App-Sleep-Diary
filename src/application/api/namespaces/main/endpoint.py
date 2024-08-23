from flask_restx import Resource
from flask_restx._http import HTTPStatus

from src.application.api.namespaces.main.schemas import MainEndpointSchema


class MainEndpoint(Resource):
    @staticmethod
    def get() -> tuple[dict, HTTPStatus]:
        return MainEndpointSchema().model_dump(), HTTPStatus.OK
