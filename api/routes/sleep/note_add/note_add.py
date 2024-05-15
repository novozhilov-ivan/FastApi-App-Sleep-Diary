from flask import request
from flask_restx import Resource

from api.CRUD.notations import create_one_note
from api.models import Notation
from api.routes import ns_sleep
from api.routes.sleep import response_model_400, response_model_422, user_id_params
from api.routes.sleep.note_add import add_note_payload, response_model_201
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNote, SleepNoteCompute
from common.pydantic_schemas.user import User


class AddNoteRoute(Resource):
    """Добавление новой записи в дневник сна"""

    @ns_sleep.doc(description=__doc__)
    @ns_sleep.expect(user_id_params, add_note_payload)
    @ns_sleep.param("payload", description=SleepNote.__doc__, _in="body")
    @ns_sleep.response(**response_model_201)
    @ns_sleep.response(**response_model_400)
    @ns_sleep.response(**response_model_422)
    def post(self):
        user = User(**request.args)
        new_note = SleepNote(**request.json)
        new_db_note = Notation(
            user_id=user.id,
            **new_note.model_dump(by_alias=True),
        )
        new_db_note = create_one_note(new_db_note)
        created_note = SleepNoteCompute.model_validate(new_db_note)
        return created_note.model_dump(mode="json"), HTTP.CREATED_201
