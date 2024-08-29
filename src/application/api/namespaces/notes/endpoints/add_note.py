from http import HTTPStatus
from typing import Any
from uuid import uuid4

from flask import request
from flask_restx import Resource
from werkzeug import Response
from werkzeug.exceptions import BadRequest

from src import service_layer
from src.application.services import DictFromJsonPayload
from src.domain import ErrorNoteAlreadyExist
from src.domain.note import (
    ErrorNoSleepDuration,
    ErrorNoteBase,
    ErrorTimePointsSequence,
)
from src.infrastructure.database import Database
from src.infrastructure.repository import ORMDiaryRepository
from src.settings import Settings


class AddNoteEndPoint(Resource):
    """Добавление новой записи в дневник"""

    NAME: str = "add note"

    @staticmethod
    def post() -> tuple[Any, HTTPStatus]:
        database = Database(Settings().POSTGRES_DB_URL)
        repo = ORMDiaryRepository(database)
        owner_id = uuid4()
        payload: dict[str, str] = DictFromJsonPayload(request).json
        try:
            service_layer.write(
                payload["bedtime_date"],
                payload["went_to_bed"],
                payload["fell_asleep"],
                payload["woke_up"],
                payload["got_up"],
                payload["no_sleep"],
                owner_id,
                repo,
            )
        except (
            ErrorNoteBase,
            ErrorTimePointsSequence,
            ErrorNoSleepDuration,
            ErrorNoteAlreadyExist,
        ) as exception:
            raise BadRequest(
                description=HTTPStatus.BAD_REQUEST.description,
                response=Response(
                    status=HTTPStatus.BAD_REQUEST,
                    response=exception.message,
                ),
            )
        return None, HTTPStatus.CREATED
