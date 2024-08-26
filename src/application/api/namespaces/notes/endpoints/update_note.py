from http import HTTPStatus

from flask_restx import Resource


class UpdateNoteEndPoint(Resource):
    """Обновление значений полей в записи из дневника"""

    NAME: str = "update note"

    @staticmethod
    def patch() -> tuple[dict, HTTPStatus]:
        return {}, HTTPStatus.OK
