import re
from datetime import date

from flask_restx import Resource, abort

from api.CRUD.notations import (
    find_user_note_by_calendar_date,
    find_user_note_by_note_id,
)
from api.models import User
from api.routes import ns_sleep
from api.routes.account import response_model_401
from api.routes.sleep.note_read import (
    ParamsDateOrInt,
    path_params,
    pattern_date,
    pattern_date_or_int,
    response_model_200,
    response_model_404,
    response_model_422,
    response_not_found_404,
    response_unprocessable_entity_422,
)
from api.utils.auth import get_current_auth_user_id_for_access
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import DateOfSleepNote, SleepNote


@ns_sleep.response(**response_model_200)
@ns_sleep.response(**response_model_401)
@ns_sleep.response(**response_model_404)
@ns_sleep.response(**response_model_422)
class NoteReadRoute(Resource):
    """Чтение записи из дневника сна по дате записи или id записи"""

    @ns_sleep.doc(
        description=__doc__,
        params=path_params,
    )
    def get(
        self,
        choice: ParamsDateOrInt,
        value: date | str,
    ):
        if not re.match(pattern_date_or_int, value) or (
            choice == ParamsDateOrInt.calendar_date.value
            and re.match(pattern_date, value) is None
        ):
            abort(
                code=HTTP.UNPROCESSABLE_ENTITY_422,
                message=response_unprocessable_entity_422,
            )

        current_user_id: int = get_current_auth_user_id_for_access()
        db_note: User | None = None

        if choice == ParamsDateOrInt.note_id.value and value.isdigit():
            db_note = find_user_note_by_note_id(
                note_id=value,
                user_id=current_user_id,
            )
        elif (
            choice == ParamsDateOrInt.calendar_date.value
            and re.match(pattern_date, value) is not None
        ):
            date_of_note = DateOfSleepNote(calendar_date=value)
            db_note = find_user_note_by_calendar_date(
                calendar_date=date_of_note.calendar_date,
                user_id=current_user_id,
            )

        if db_note is None:
            abort(
                code=HTTP.NOT_FOUND_404,
                message=response_not_found_404,
            )
        note = SleepNote.model_validate(db_note)
        return note.model_dump(mode="json"), HTTP.OK_200
