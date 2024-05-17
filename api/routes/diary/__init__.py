from flask_restx import Namespace

from api.exceptions.handlers import handler_unprocessable_entity_422
from api.utils.payload import create_payload_from_model
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.errors.message import ErrorResponse
from common.pydantic_schemas.sleep.diary import SleepDiaryModel, SleepDiaryModelEmpty
from common.pydantic_schemas.user import User

ns_diary = Namespace(
    name="Sleep diary",
    description="Дневник сна, все записи и статистика",
    path="/",
    decorators=[
        # validate_auth_token,
    ],
)
ns_diary.errorhandler(handler_unprocessable_entity_422)

response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_diary,
    model=SleepDiaryModel,
)
response_model_400 = response_schema(
    code=HTTP.BAD_REQUEST_400,
    ns=ns_diary,
    model=ErrorResponse,
)
response_model_404 = response_schema(
    code=HTTP.NOT_FOUND_404,
    ns=ns_diary,
    model=SleepDiaryModelEmpty,
)
response_model_422 = response_schema(
    code=HTTP.UNPROCESSABLE_ENTITY_422,
    ns=ns_diary,
    model=ErrorResponse,
)

user_id_params = create_payload_from_model("args", User)

from api.routes.diary.diary import DiaryRoute  # noqa

diary_endpoint = "diary"
ns_diary.add_resource(
    DiaryRoute,
    f"/{diary_endpoint}",
    endpoint=diary_endpoint,
)
