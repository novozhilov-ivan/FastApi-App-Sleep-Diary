from typing import Sequence

from flask import Response
from flask_restx import Resource
from flask_restx.reqparse import RequestParser

from sleep_diary_api.Routes import ns_sleep
from sleep_diary_api import Api_schema_models
from sleep_diary_api.Utils.manage_notes import convert_notes, slice_on_week
from src.pydantic_schemas.notes.sleep_diary import SleepDiaryEntriesModel, SleepDiaryEntriesCompute
from src.pydantic_schemas.notes.sleep_notes import SleepNote, SleepNoteModel
from sleep_diary_api.CRUD.notation_queries import get_all_notations_of_user


@ns_sleep.route("/sleep", endpoint='sleep')
class SleepPage(Resource):
    @ns_sleep.response(
        code=200,
        description='Получение всех записей и статистики пользователя по записям из дневника сна.',
        model=Api_schema_models.sleep_get_all
    )
    @ns_sleep.doc(
        shortcut='Все записи пользователя из дневника сна.',
        params={'user_id': 'Id пользователя для получения его записей.'}
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

        sleep_diary = SleepDiaryEntriesCompute(weeks=pd_weeks)

        response_model = SleepDiaryEntriesModel.model_validate(sleep_diary)
        return Response(response_model.model_dump_json(indent=2))

    @ns_sleep.response(
        code=200,
        description='Получение новой созданной записи.',
        model=Api_schema_models.sleep_post_created
    )
    @ns_sleep.expect(Api_schema_models.sleep_post_requested)
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
