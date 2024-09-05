from typing import Any

from flask import request
from flask_restx import abort

from src.CRUD.sleep_note_table import update_user_note
from src.models import SleepNoteOrm
from src.pydantic_schemas.sleep.notes import (
    SleepNote,
    SleepNoteMeta,
    SleepNoteOptional,
)
from src.routes.account import response_model_401
from src.routes.edit import response_model_422
from src.routes.notes import ns_notes
from src.routes.notes.note_find_by_id import (
    response_model_200,
    response_model_404,
    response_not_found_404,
)
from src.routes.notes.note_update import update_note_params
from src.utils.auth import UserActions
from src.utils.status_codes import HTTP


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
            owner_oid=self.current_user_id,
            **request.args,
        )
        payload: Any | dict = request.json
        note = SleepNoteOptional(**payload)

        updated_db_note: SleepNoteOrm | None = update_user_note(
            id=note_meta.id,
            user_id=note_meta.owner_oid,
            note_values=note.model_dump(exclude_none=True),
        )
        if updated_db_note is None:
            abort(
                code=HTTP.NOT_FOUND_404,
                message=response_not_found_404,
            )
        response_note = SleepNote.model_validate(updated_db_note)
        return response_note.model_dump(mode="json"), HTTP.OK_200
