from flask_restx import Namespace

from api.utils.jwt import validate_auth_token
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.errors.message import ErrorResponse

ns_edit = Namespace(
    name="Edit diary",
    description="Изменения в дневнике сна",
    path="/edit",
    decorators=[
        validate_auth_token,
    ],
)
response_not_found_404 = "User or sleep notes not found"
response_model_404 = response_schema(
    ns=ns_edit,
    code=HTTP.NOT_FOUND_404,
    description=response_not_found_404,
)
response_model_422 = response_schema(
    ns=ns_edit,
    code=HTTP.UNPROCESSABLE_ENTITY_422,
    model=ErrorResponse,
)
