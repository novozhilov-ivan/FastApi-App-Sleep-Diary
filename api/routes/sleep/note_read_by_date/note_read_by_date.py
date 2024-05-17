from datetime import date

from flask_restx import Resource, abort

from api.CRUD.notations import (
    find_user_note_by_calendar_date,
)
from api.routes import ns_sleep
from api.routes.account import response_model_401
from api.routes.sleep.note_read_by_date import (
    path_params,
    response_model_200,
    response_model_404,
    response_not_found_404,
)
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import DateOfSleepNote, SleepNote


@ns_sleep.response(**response_model_200)
@ns_sleep.response(**response_model_401)
@ns_sleep.response(**response_model_404)
class NoteReadByDateRoute(Resource):
    """Чтение записи из дневника сна по дате"""

    @ns_sleep.doc(
        description=__doc__,
        params=path_params,
    )
    def get(self, calendar_date: date):
        # current_user_id: int = get_current_auth_user_id_for_access()
        current_user_id: int = 2
        print(current_user_id)
        date_of_note = DateOfSleepNote(calendar_date=calendar_date)
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
