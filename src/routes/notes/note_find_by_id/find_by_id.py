from flask_restx import Resource, abort

from src.CRUD.sleep_note_table import find_user_note_by_note_id
from src.models import SleepNoteOrm
from src.pydantic_schemas.sleep.notes import SleepNote
from src.routes.account import response_model_401
from src.routes.notes import ns_notes
from src.routes.notes.note_find_by_id import (
    path_params,
    response_model_200,
    response_model_404,
    response_not_found_404,
)
from src.utils.auth import UserActions
from src.utils.status_codes import HTTP


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
