from flask import request

from api.CRUD.notations import create_one_note
from api.models import Notation
from api.routes.diary import response_model_400, response_model_422, user_id_params
from api.routes.notes import ns_notes
from api.routes.notes.note_add import add_note_payload, response_model_201
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNote, SleepNoteWithStats
from common.pydantic_schemas.user import User


class AddNote:
    """Добавление новой записи в дневник сна"""

    @ns_notes.doc(description=__doc__)
    @ns_notes.expect(user_id_params, add_note_payload)
    @ns_notes.param("payload", description=SleepNote.__doc__, _in="body")
    @ns_notes.response(**response_model_201)
    @ns_notes.response(**response_model_400)
    @ns_notes.response(**response_model_422)
    def post(self):
        user = User(**request.args)
        new_note = SleepNote(**request.json)
        new_db_note = Notation(
            user_id=user.id,
            **new_note.model_dump(by_alias=True),
        )
        new_db_note = create_one_note(new_db_note)
        created_note = SleepNoteWithStats.model_validate(new_db_note)
        return created_note.model_dump(mode="json"), HTTP.CREATED_201
