from flask import Response, request
from flask_restx import Resource

from api.models import Notation
from api.routes.sleep import (
    ns_sleep,
    # Success response schemas
    get_all_notes_response_model_200,
    post_new_note_response_model_201,
    # Payloads
    new_note_payload,
    user_id_params,
    # Errors
    get_all_notes_response_model_404,
    response_model_422,
    response_model_400,
)
from api.utils.manage_notes import (
    convert_db_notes_to_pydantic_model_notes,
    slice_on_week,
)
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.diary import SleepDiaryModel, SleepDiaryCompute
from common.pydantic_schemas.sleep.notes import SleepNoteCompute, SleepNote
from common.pydantic_schemas.user import User
from api.CRUD.notation_queries import read_all_user_notes, create_one_note


@ns_sleep.response(**response_model_422)
@ns_sleep.response(**response_model_400)
class SleepRoute(Resource):
    @ns_sleep.doc(description="Получение всех записей дневника сна")
    @ns_sleep.expect(user_id_params)
    @ns_sleep.response(**get_all_notes_response_model_200)
    @ns_sleep.response(**get_all_notes_response_model_404)
    def get(self):
        args = request.args.to_dict()
        user = User(**args)
        db_notes = read_all_user_notes(user.id)
        pd_notes = convert_db_notes_to_pydantic_model_notes(db_notes)
        pd_weeks = slice_on_week(pd_notes)
        sleep_diary = SleepDiaryCompute(weeks=pd_weeks)
        response = SleepDiaryModel.model_validate(sleep_diary)
        status = HTTP.NOT_FOUND_404
        if db_notes:
            status = HTTP.OK_200
        response = response.model_dump_json()
        return Response(response, status, content_type="application/json")

    @ns_sleep.doc(description="Добавление новой записи в дневник сна")
    @ns_sleep.expect(user_id_params, new_note_payload)
    @ns_sleep.param("payload", "Новая запись в дневник сна", _in="body")
    @ns_sleep.response(**post_new_note_response_model_201)
    def post(self):
        new_note = SleepNote(**ns_sleep.payload)
        args = request.args.to_dict()
        user = User(**args)
        new_db_note = Notation(user_id=user.id, **new_note.model_dump(by_alias=True))
        new_db_note = create_one_note(new_db_note)
        response = SleepNoteCompute(**new_db_note.dict())
        response = response.model_dump_json()
        return Response(response, HTTP.CREATED_201, content_type="application/json")
