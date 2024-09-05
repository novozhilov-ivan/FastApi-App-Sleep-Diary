from typing import Any

from legacy_src.CRUD.sleep_note_table import create_one_note
from legacy_src.models.models import SleepNoteOrm
from legacy_src.pydantic_schemas.sleep.notes import SleepNote, SleepNoteWithStats
from legacy_src.routes.notes import ns_notes, response_model_400, response_model_422
from legacy_src.routes.notes.note_add import add_note_payload, response_model_201
from legacy_src.utils.auth import UserActions
from legacy_src.utils.status_codes import HTTP


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
        payload: Any | dict = request.json
        new_note = SleepNote(**payload)
        new_db_note = SleepNoteOrm(
            owner_oid=self.current_user_id,
            **new_note.model_dump(),
        )
        new_db_note = create_one_note(new_db_note)
        created_note = SleepNoteWithStats.model_validate(new_db_note)
        return created_note.model_dump(mode="json"), HTTP.CREATED_201
