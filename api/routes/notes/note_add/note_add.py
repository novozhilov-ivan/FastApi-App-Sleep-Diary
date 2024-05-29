from flask import request

from api.CRUD.dream_notes import create_one_note
from api.models import DreamNote
from api.routes.diary import response_model_400, response_model_422
from api.routes.notes import ns_notes
from api.routes.notes.note_add import add_note_payload, response_model_201
from api.utils.auth import UserActions
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNote, SleepNoteWithStats


class AddNote(UserActions):
    """Добавление новой записи в дневник сна"""

    # TODO Изменить объявление param

    @ns_notes.doc(description=__doc__)
    @ns_notes.expect(add_note_payload)
    @ns_notes.param("payload", description=SleepNote.__doc__, _in="body")
    @ns_notes.response(**response_model_201)
    @ns_notes.response(**response_model_400)
    @ns_notes.response(**response_model_422)
    def post(self):
        new_note = SleepNote(**request.json)
        new_db_note = DreamNote(
            user_id=self.current_user_id,
            **new_note.model_dump(),
        )
        new_db_note = create_one_note(new_db_note)
        created_note = SleepNoteWithStats.model_validate(new_db_note)
        return created_note.model_dump(mode="json"), HTTP.CREATED_201
