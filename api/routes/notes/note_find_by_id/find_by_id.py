from flask_restx import Resource, abort

from api.CRUD.sleep_note_table import find_user_note_by_note_id
from api.models import SleepNoteOrm
from api.routes.account import response_model_401
from api.routes.notes import ns_notes
from api.routes.notes.note_find_by_id import (
    path_params,
    response_model_200,
    response_model_404,
    response_not_found_404,
)
from api.utils.auth import UserActions
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNote


class NoteFindById(Resource, UserActions):
    """Чтение записи из дневника сна по id"""

    @ns_notes.response(**response_model_200)
    @ns_notes.response(**response_model_401)
    @ns_notes.response(**response_model_404)
    @ns_notes.doc(
        description=__doc__,
        params=path_params,
    )
    def get(self, id: int):
        db_note: SleepNoteOrm | None = find_user_note_by_note_id(
            id=id,
            user_id=self.current_user_id,
        )
        if db_note is None:
            abort(
                code=HTTP.NOT_FOUND_404,
                message=response_not_found_404,
            )
        note = SleepNote.model_validate(db_note)
        return note.model_dump(mode="json"), HTTP.OK_200
