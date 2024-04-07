from flask_restx import Namespace

from api.schemas.flask_api_models import response_schema, flask_restx_schema
from api.schemas.payload import create_payload
from api.exceptions.handler_400 import handler_bad_request_400, handler_unprocessable_entity_422
from common.pydantic_schemas.errors.message import ErrorResponse

from common.pydantic_schemas.sleep.diary import SleepDiaryModel, SleepDiaryModelEmpty
from common.pydantic_schemas.sleep.notes import SleepNote, SleepNoteModel
from common.pydantic_schemas.user import User

ns_sleep = Namespace(
    name='sleep',
    description='Описание sleep page',
    path='/',
    validate=True
)
# Errors
ns_sleep.default_error_handler = handler_bad_request_400
ns_sleep.errorhandler(handler_unprocessable_entity_422)

# Get
get_all_notes_response_model_200 = response_schema(
    code=200,
    ns=ns_sleep,
    model=SleepDiaryModel
)
get_all_notes_response_model_404 = response_schema(
    code=404,
    ns=ns_sleep,
    model=SleepDiaryModelEmpty,
)
get_all_notes_param = create_payload('args', ns_sleep, User)

# Post
new_note_expect_payload_model = flask_restx_schema(ns_sleep, SleepNote)
post_new_note_response_model_201 = response_schema(
    code=201,
    ns=ns_sleep,
    model=SleepNoteModel,
)

response_model_422 = response_schema(
    code=422,
    ns=ns_sleep,
    model=ErrorResponse,
)
response_model_400 = response_schema(
    code=400,
    ns=ns_sleep,
    model=ErrorResponse,
)

from api.routes.sleep.route_sleep import SleepRoute

ns_sleep.add_resource(SleepRoute, '/sleep')
