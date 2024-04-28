from flask_restx import Namespace

from api.exceptions.handlers import handler_unprocessable_entity_422
from api.schemas.flask_api_models import response_schema
from api.schemas.payload import create_payload_from_model
from common.baseclasses.status_codes import HTTP
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
ns_sleep.errorhandler(handler_unprocessable_entity_422)

# Get models
get_all_notes_response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_sleep,
    model=SleepDiaryModel
)
get_all_notes_response_model_404 = response_schema(
    code=HTTP.NOT_FOUND_404,
    ns=ns_sleep,
    model=SleepDiaryModelEmpty,
)
user_id_params = create_payload_from_model('args', User)

# Post
new_note_payload = create_payload_from_model('json', SleepNote)
post_new_note_response_model_201 = response_schema(
    code=HTTP.CREATED_201,
    ns=ns_sleep,
    model=SleepNoteModel,
)

response_model_422 = response_schema(
    code=HTTP.UNPROCESSABLE_ENTITY_422,
    ns=ns_sleep,
    model=ErrorResponse,
)
response_model_400 = response_schema(
    code=HTTP.BAD_REQUEST_400,
    ns=ns_sleep,
    model=ErrorResponse,
)

from api.routes.sleep.route_sleep import SleepRoute

ns_sleep.add_resource(SleepRoute, '/sleep')
