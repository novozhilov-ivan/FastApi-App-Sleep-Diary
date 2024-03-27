from flask_restx import Namespace

from sleep_diary_api.Api_schemas.flask_api_models import response_schema
from sleep_diary_api.Routes import general_path_prefix

from src.pydantic_schemas.notes.sleep_diary import SleepDiaryModel
from src.pydantic_schemas.notes.sleep_notes import SleepNote, SleepNoteModel


ns_sleep = Namespace(
    name='sleep',
    description='Описание sleep page',
    path=general_path_prefix
)

# /sleep
# Get
get_all_notes_response_model_200 = response_schema(
    200,
    'Получение всех записей пользователя из дневника сна',
    ns_sleep,
    SleepDiaryModel
)

# Post
post_new_note_expect_payload_model = response_schema(
    200,
    'Схема создания новой записи в дневник сна',
    ns_sleep,
    SleepNote
)
post_new_note_response_model_200 = response_schema(
    201,
    'Успешно созданная запись в дневнике сна',
    ns_sleep,
    SleepNoteModel
)

from sleep_diary_api.Routes.sleep.route_sleep import SleepRoute
ns_sleep.add_resource(SleepRoute, '/sleep')
