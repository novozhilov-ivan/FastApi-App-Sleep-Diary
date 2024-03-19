from flask import Response
from flask_restx import Resource, Namespace
from pydantic import TypeAdapter

from sleep_diary_api.Utils.flask_api_models import flask_restx_schema
from src.pydantic_schemas.sleep_notes import SleepDiaryEntries, SleepNoteBase, WeeksSleepDiary
from sleep_diary_api.CRUD.notation_queries import get_all_notations_of_user

ns_sleep = Namespace('api')
all_sleep_notes_response_model = flask_restx_schema(ns_sleep, SleepDiaryEntries)


@ns_sleep.route("/sleep")
@ns_sleep.response(
    code=200,
    description='Получение записей и статистики по записям из дневника сна.',
    model=all_sleep_notes_response_model
)
class SleepPage(Resource):
    @ns_sleep.doc('Все записи из дневника сна.')
    def get(self):
        user_id = 1
        all_notes = get_all_notations_of_user(user_id)

        type_adapter = TypeAdapter(list[SleepNoteBase])
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
