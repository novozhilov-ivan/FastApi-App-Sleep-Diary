from flask import Response, request
from flask_restx import Resource
from pydantic import ValidationError

from api.models import Notation
from api.routes.sleep import (
    ns_sleep,
    get_all_notes_response_model_200,
    post_new_note_response_model_201,
    new_note_expect_payload_model,
    get_all_notes_param, get_all_notes_response_model_404,
)
from api.utils.manage_notes import convert_notes, slice_on_week
from common.pydantic_schemas.notes.sleep_diary import SleepDiaryModel, SleepDiaryCompute
from common.pydantic_schemas.notes.sleep_notes import SleepNoteCompute, SleepNote
from common.pydantic_schemas.user import User
from api.CRUD.notation_queries import get_all_notations_of_user, post_new_note


class SleepRoute(Resource):
    @ns_sleep.doc(description='Получение всех записей дневника сна по id пользователя')
    @ns_sleep.expect(get_all_notes_param)
    @ns_sleep.response(**get_all_notes_response_model_200)
    @ns_sleep.response(**get_all_notes_response_model_404)
    def get(self):
        args = request.args.to_dict()
        try:
            user = User(**args)
        except ValidationError as e:
            status = 400
            response = e.json(
                    indent=4,
                    include_url=False,
                    include_context=False,
                    include_input=False
            )
        else:
            user_id = user.id
            db_notes = get_all_notations_of_user(user_id)
            pd_notes = convert_notes(db_notes)
            pd_weeks = slice_on_week(pd_notes)
            sleep_diary = SleepDiaryCompute(weeks=pd_weeks)
            response = SleepDiaryModel.model_validate(sleep_diary)
            status = 404
            if db_notes:
                status = 200
            response = response.model_dump_json()
        return Response(response, status, content_type='application/json')

    @ns_sleep.doc(description='Добавление новой записи в дневник сна')
    @ns_sleep.expect(new_note_expect_payload_model)
    @ns_sleep.param('payload', 'Новая запись в дневник сна', _in='body')
    @ns_sleep.response(**post_new_note_response_model_201)
    def post(self):
        status = 400
        try:
            new_note = SleepNote(**ns_sleep.payload)
            new_db_note = Notation(user_id=1, **new_note.model_dump(by_alias=True))
            new_db_note = post_new_note(new_db_note)
        except ValidationError as e:
            response = e.json(
                indent=4,
                include_url=False,
                include_context=False,
                include_input=False
            )
        else:
            response = SleepNoteCompute(**new_db_note.dict())
            response = response.model_dump_json(indent=4)
            status = 201
        return Response(response, status, content_type='application/json')
