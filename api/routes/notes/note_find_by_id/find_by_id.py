from flask_restx import Resource, abort

from api.CRUD.notations import (
    find_user_note_by_note_id,
)
from api.routes.account import response_model_401
from api.routes.notes import ns_notes
from api.routes.notes.note_find_by_id import (
    path_params,
    response_model_200,
    response_model_404,
    response_not_found_404,
)
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNote


@ns_notes.response(**response_model_200)
@ns_notes.response(**response_model_401)
@ns_notes.response(**response_model_404)
class NoteFindById(Resource):
    """Чтение записи из дневника сна по id"""

    @ns_notes.doc(
        description=__doc__,
        params=path_params,
    )
    def get(self, note_id: int | str):
        # current_user_id: int = get_current_auth_user_id_for_access()
        current_user_id: int = 2
        db_note = find_user_note_by_note_id(
            note_id=note_id,
            user_id=current_user_id,
        )
        if db_note is None:
            abort(
                code=HTTP.NOT_FOUND_404,
                message=response_not_found_404,
            )
        note = SleepNote.model_validate(db_note)
        return note.model_dump(mode="json"), HTTP.OK_200
