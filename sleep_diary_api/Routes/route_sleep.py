from flask import Response
from flask_restx import Resource, Namespace
from flask_restx.reqparse import RequestParser

from pydantic import TypeAdapter

from sleep_diary_api.Utils.flask_api_models import flask_restx_schema
from src.pydantic_schemas.sleep_notes import (
    SleepDiaryEntries,
    SleepNoteDateTimes,
    SleepNote,
    WeeksSleepDiary
)
from sleep_diary_api.CRUD.notation_queries import get_all_notations_of_user

ns_sleep = Namespace('api')

# Get
all_sleep_notes_response_model = flask_restx_schema(ns_sleep, SleepDiaryEntries)

# Post
new_note_request = flask_restx_schema(ns_sleep, SleepNoteDateTimes)
get_created_note_response_model = flask_restx_schema(ns_sleep, SleepNote)


@ns_sleep.route("/sleep", endpoint='sleep')
class SleepPage(Resource):
    @ns_sleep.response(
        code=200,
        description='Получение всех записей и статистики пользователя по записям из дневника сна.',
        model=all_sleep_notes_response_model
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

        all_notes = get_all_notations_of_user(user_id)

        type_adapter = TypeAdapter(list[SleepNote])
        all_validate_notes = type_adapter.validate_python(all_notes, from_attributes=True)

        notes_count = len(all_validate_notes)
        weeks_count = notes_count // 7
        weeks = []

        for week in range(weeks_count):
            f_day_in_week = week * 7
            last_day_in_week = f_day_in_week + 7
            if last_day_in_week > notes_count:
                last_day_in_week = notes_count

            days = all_validate_notes[f_day_in_week:last_day_in_week]
            week = WeeksSleepDiary(
                weekly_statistics=None,
                days=days
            )
            weeks.append(week)

        sleep_diary = SleepDiaryEntries(
            notes_count=notes_count,
            weeks_count=weeks_count,
            weeks=weeks
        )

        response = sleep_diary.model_dump_json(
            indent=4,
            by_alias=True
        )
        return Response(response)

    @ns_sleep.response(
        code=200,
        description='Получение новой созданной записи.',
        model=get_created_note_response_model
    )
    @ns_sleep.expect(new_note_request)
    def post(self):
        user_id = 1
        parser = RequestParser()
        fields = list(SleepNoteDateTimes.model_fields.keys())
        for field in fields:
            parser.add_argument(
                name=field,
                type=str,
                # required=True,
                location='json',
            )

        args = parser.parse_args()
        new_sleep_note = SleepNote(
            id=0,
            user_id=user_id,
            **args
        )
        response = new_sleep_note.model_dump_json(
            indent=4,
            by_alias=True
        )
        return Response(response)
