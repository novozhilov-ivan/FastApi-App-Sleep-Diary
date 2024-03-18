from flask_restx import Resource, Namespace

from sleep_diary_api.Utils.flask_api_models import flask_restx_schema
from src.pydantic_schemas.sleep_notes import SleepDiaryEntries

ns_sleep = Namespace('api')


sleep_diary_response_model = flask_restx_schema(ns_sleep, SleepDiaryEntries)


@ns_sleep.route("/sleep")
@ns_sleep.response(
    code=200,
    description='Получение записей и статистики по записям из дневника сна.',
    model=sleep_diary_response_model
)
class SleepPage(Resource):
    @ns_sleep.doc('Все записи из дневника сна.')
    def get(self):
        return {}
