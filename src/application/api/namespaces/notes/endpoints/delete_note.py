from http import HTTPStatus

from flask_restx import Resource


class DeleteNoteEndPoint(Resource):
    """Удаление записи из дневника по oid"""

    NAME: str = "delete note"

    @staticmethod
    def delete() -> tuple[None, HTTPStatus]:
        return None, HTTPStatus.NO_CONTENT
