from flask import request

from api.CRUD.notations import delete_user_note
from api.routes.account import response_model_401
from api.routes.edit import response_model_422
from api.routes.notes import ns_notes
from api.routes.notes.note_delete import note_id_params, response_model_204
from api.utils.auth import get_current_auth_user_id_for_access
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNoteMeta


@ns_notes.response(**response_model_204)
@ns_notes.response(**response_model_401)
@ns_notes.response(**response_model_422)
class DeleteNote:
    """Удаление записи из дневника по id"""

    @ns_notes.doc(
        description=__doc__,
        params=note_id_params,
    )
    def delete(self):
        current_user_id: int = get_current_auth_user_id_for_access()
        note = SleepNoteMeta(
            user_id=current_user_id,
            **request.args,
        )
        delete_user_note(
            user_id=note.user_id,
            note_id=note.id,
        )
        return None, HTTP.NO_CONTENT_204
