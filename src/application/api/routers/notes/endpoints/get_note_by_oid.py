from http import HTTPStatus
from uuid import UUID

from flask_restx import Resource


class GetNoteByOidEndPoint(Resource):
    """Получение записи из дневника по oid"""

    NAME: str = "get note by oid"

    @staticmethod
    def get(oid: UUID) -> tuple[dict, HTTPStatus]:
        return {}, HTTPStatus.OK
