from flask_restx import Namespace

from src.exceptions.handlers import handler_unprocessable_entity_422
from src.pydantic_schemas.errors.message import ErrorResponse
from src.pydantic_schemas.sleep.diary import SleepDiaryModel, SleepDiaryModelEmpty
from src.utils.jwt import validate_auth_token
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP

ns_diary: Namespace = Namespace(
    name="Sleep diary",
    description="Дневник сна, все записи и статистика",
    path="/diary",
    decorators=[
        validate_auth_token,
    ],
)
ns_diary.errorhandler(handler_unprocessable_entity_422)

response_model_200: dict = response_schema(
    code=HTTP.OK_200,
    ns=ns_diary,
    model=SleepDiaryModel,
)
response_model_400: dict = response_schema(
    code=HTTP.BAD_REQUEST_400,
    ns=ns_diary,
    model=ErrorResponse,
)
response_model_404: dict = response_schema(
    code=HTTP.NOT_FOUND_404,
    ns=ns_diary,
    model=SleepDiaryModelEmpty,
)
response_model_422: dict = response_schema(
    code=HTTP.UNPROCESSABLE_ENTITY_422,
    ns=ns_diary,
    model=ErrorResponse,
)

from src.routes.diary.diary import DiaryRoute  # noqa

diary_endpoint = "diary"
ns_diary.add_resource(
    DiaryRoute,
    "",
    endpoint=diary_endpoint,
)
