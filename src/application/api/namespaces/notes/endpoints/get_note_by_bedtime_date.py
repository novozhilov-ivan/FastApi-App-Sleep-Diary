from datetime import date
from http import HTTPStatus

from flask_restx import Resource


class GetNoteByBedtimeDateEndPoint(Resource):
    """Получение записи из дневника по дате сна"""

    NAME: str = "get note by bedtime date"

    @staticmethod
    def get(bedtime_date: date) -> tuple[dict, HTTPStatus]:
        return {}, HTTPStatus.OK
