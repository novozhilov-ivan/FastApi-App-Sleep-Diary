from flask import Response
from flask_restx import Resource
from flask_restx.reqparse import RequestParser

from sleep_diary_api.Routes.sleep import (
    ns_sleep,
    get_all_notes_response_model_200,
    post_new_note_response_model_200,
    post_new_note_expect_payload_model,
)
from sleep_diary_api.Utils.manage_notes import convert_notes, slice_on_week
from src.pydantic_schemas.notes.sleep_diary import SleepDiaryModel, SleepDiaryCompute
from src.pydantic_schemas.notes.sleep_notes import SleepNote, SleepNoteModel
from sleep_diary_api.CRUD.notation_queries import get_all_notations_of_user


class SleepRoute(Resource):
    @ns_sleep.response(**get_all_notes_response_model_200)
    @ns_sleep.doc(
        shortcut='Все записи пользователя из дневника сна.',
        params={'user_id': 'Id пользователя дневника сна.'}
    )
    def get(self):
        parser = RequestParser()
        parser.add_argument(
            name='user_id',
            type=int,
            required=True,
            location='values'
        )
        args = parser.parse_args()
        user_id = args['user_id']

        db_notes = get_all_notations_of_user(user_id)

        pd_notes = convert_notes(db_notes)
        pd_weeks = slice_on_week(pd_notes)

        sleep_diary = SleepDiaryCompute(weeks=pd_weeks)

        response_model = SleepDiaryModel.model_validate(sleep_diary)

        return Response(
            response=response_model.model_dump_json(),
            status=200 if sleep_diary.weeks else 404,
            content_type='application/json',
        )

    @ns_sleep.response(**post_new_note_response_model_200)
    # не работает
    @ns_sleep.expect(post_new_note_expect_payload_model)
    def post(self):
        user_id = 1
        parser = RequestParser()
        fields = list(SleepNote.model_fields.keys())
        for field in fields:
            parser.add_argument(
                name=field,
                type=str,
                required=True,
                location='json',
            )

        args = parser.parse_args()
        new_sleep_note = SleepNoteModel(
            id=0,
            user_id=user_id,
            **args
        )
        response = new_sleep_note.model_dump_json(
            indent=4,
            by_alias=True
        )
        return Response(response)
