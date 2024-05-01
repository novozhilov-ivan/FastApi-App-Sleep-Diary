from flask_restx import Namespace

from api.exceptions.handlers import handler_unprocessable_entity_422
from api.schemas.flask_api_models import response_schema
from api.schemas.payload import create_payload_from_model
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.errors.message import ErrorResponse
from common.pydantic_schemas.sleep.diary import SleepDiaryModel
from common.pydantic_schemas.user import User

ns_sleep = Namespace(
    name="sleep",
    description="Описание sleep page",
    path="/sleep",
)
ns_sleep.errorhandler(handler_unprocessable_entity_422)

response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_sleep,
    model=SleepDiaryModel,
)
response_model_400 = response_schema(
    code=HTTP.BAD_REQUEST_400,
    ns=ns_sleep,
    model=ErrorResponse,
)
response_model_422 = response_schema(
    code=HTTP.UNPROCESSABLE_ENTITY_422,
    ns=ns_sleep,
    model=ErrorResponse,
)

user_id_params = create_payload_from_model("args", User)
