from flask_restx import Namespace

from api.exceptions.handlers import handler_unprocessable_entity_422
from api.utils.jwt import validate_auth_token
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.errors.message import ErrorResponse
from common.pydantic_schemas.sleep.diary import SleepDiaryModel, SleepDiaryModelEmpty

ns_diary = Namespace(
    name="Sleep diary",
    description="Дневник сна, все записи и статистика",
    path="/diary",
    decorators=[
        validate_auth_token,
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

from api.routes.diary.diary import DiaryRoute  # noqa

diary_endpoint = "diary"
ns_diary.add_resource(
    DiaryRoute,
    "",
    endpoint=diary_endpoint,
)
