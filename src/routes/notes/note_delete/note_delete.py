from flask import request

from src.CRUD.sleep_note_table import delete_user_note
from src.pydantic_schemas.sleep.notes import SleepNoteMeta
from src.routes.account import response_model_401
from src.routes.edit import response_model_422
from src.routes.notes import ns_notes
from src.routes.notes.note_delete import note_id_params, response_model_204
from src.utils.auth import UserActions
from src.utils.status_codes import HTTP


class DeleteNote(UserActions):
    """Удаление записи из дневника по id"""

    @ns_notes.response(**response_model_204)
    @ns_notes.response(**response_model_401)
    @ns_notes.response(**response_model_422)
    @ns_notes.doc(
        description=__doc__,
        params=note_id_params,
    )
    def delete(self):
        note = SleepNoteMeta(
            owner_id=self.current_user_id,
            **request.args,
        )
        delete_user_note(
            id=note.id,
            user_id=note.owner_id,
        )
        return None, HTTP.NO_CONTENT_204
