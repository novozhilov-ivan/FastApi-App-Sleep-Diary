from flask import request

from api.CRUD.dream_notes import delete_user_note
from api.routes.account import response_model_401
from api.routes.edit import response_model_422
from api.routes.notes import ns_notes
from api.routes.notes.note_delete import note_id_params, response_model_204
from api.utils.auth import UserActions
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNoteMeta


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
            user_id=self.current_user_id,
            **request.args,
        )
        delete_user_note(**note.model_dump())
        return None, HTTP.NO_CONTENT_204
