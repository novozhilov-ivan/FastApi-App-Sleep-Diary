from flask_restx import Namespace

from sleep_diary_api.Api_schemas.flask_api_models import response_schema, flask_restx_schema
from sleep_diary_api.Api_schemas.payload import create_payload

from src.pydantic_schemas.notes.sleep_diary import SleepDiaryModel
from src.pydantic_schemas.notes.sleep_notes import SleepNote, SleepNoteModel
from src.pydantic_schemas.user import User

ns_sleep = Namespace(
    name='sleep',
    description='Описание sleep page',
    path='/',
    validate=True
)

# Get
get_all_notes_response_model_200 = response_schema(
    code=200,
    ns=ns_sleep,
    model=SleepDiaryModel,
    description='Модель всех записей дневника сна пользователя',
)
get_all_notes_param = create_payload('args', ns_sleep, User)

# Post
new_note_expect_payload_model = flask_restx_schema(ns_sleep, SleepNote)
post_new_note_response_model_201 = response_schema(
    code=201,
    ns=ns_sleep,
    model=SleepNoteModel,
    description='Модель успешно созданной записи в дневнике сна',
)

from sleep_diary_api.Routes.sleep.route_sleep import SleepRoute
ns_sleep.add_resource(SleepRoute, '/sleep')
