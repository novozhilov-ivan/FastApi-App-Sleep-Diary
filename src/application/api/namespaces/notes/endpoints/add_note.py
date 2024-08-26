from http import HTTPStatus

from flask_restx import Resource


class AddNoteEndPoint(Resource):
    """Добавление новой записи в дневник"""

    NAME: str = "add note"

    @staticmethod
    def post() -> tuple[None, HTTPStatus]:
        return None, HTTPStatus.CREATED
