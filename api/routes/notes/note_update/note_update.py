from flask import request
from flask_restx import abort

from api.CRUD.sleep_note_table import update_user_note
from api.models import SleepNoteOrm
from api.routes.account import response_model_401
from api.routes.edit import response_model_422
from api.routes.notes import ns_notes
from api.routes.notes.note_delete import note_id_params
from api.routes.notes.note_find_by_id import (
    response_model_200,
    response_model_404,
    response_not_found_404,
)
from api.routes.notes.note_update import update_note_params
from api.utils.auth import UserActions
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import (
    SleepNote,
    SleepNoteMeta,
    SleepNoteOptional,
)


class UpdateNote(UserActions):
    """Редактирование существующей записи из дневника"""

    @ns_notes.response(**response_model_200)
    @ns_notes.response(**response_model_401)
    @ns_notes.response(**response_model_404)
    @ns_notes.response(**response_model_422)
    @ns_notes.doc(
        description=__doc__,
        params={
            **note_id_params,
            **update_note_params,
        },
    )
    def patch(self):
        note_meta = SleepNoteMeta(
            owner_id=self.current_user_id,
            **request.args,
        )
        note = SleepNoteOptional(**request.json)

        updated_db_note: SleepNoteOrm | None = update_user_note(
            id=note_meta.id,
            user_id=note_meta.owner_id,
            note_values=note.model_dump(exclude_none=True),
        )
        if updated_db_note is None:
            abort(
                code=HTTP.NOT_FOUND_404,
                message=response_not_found_404,
            )
        note = SleepNote.model_validate(updated_db_note)
        return note.model_dump(mode="json"), HTTP.OK_200
