from datetime import date

from flask_restx import Resource, abort

from api.CRUD.dream_notes import find_user_note_by_calendar_date
from api.models import DreamNote
from api.routes.account import response_model_401
from api.routes.notes import ns_notes
from api.routes.notes.note_find_by_date import (
    path_params,
    response_model_200,
    response_model_404,
    response_not_found_404,
)
from api.utils.auth import UserActions
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import (
    SleepNote,
    SleepNoteOptional,
)


class NoteFindByDate(Resource, UserActions):
    """Чтение записи из дневника сна по дате"""

    @ns_notes.response(**response_model_200)
    @ns_notes.response(**response_model_401)
    @ns_notes.response(**response_model_404)
    @ns_notes.doc(
        description=__doc__,
        params=path_params,
    )
    def get(self, sleep_date: date):
        date_of_note = SleepNoteOptional(sleep_date=sleep_date)
        db_note: DreamNote | None = find_user_note_by_calendar_date(
            sleep_date=date_of_note.sleep_date,
            user_id=self.current_user_id,
        )
        if db_note is None:
            abort(
                code=HTTP.NOT_FOUND_404,
                message=response_not_found_404,
            )
        note = SleepNote.model_validate(db_note)
        return note.model_dump(mode="json"), HTTP.OK_200
