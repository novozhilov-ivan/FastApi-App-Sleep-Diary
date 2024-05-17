from flask_restx import Namespace

from api.exceptions.handlers import handler_unprocessable_entity_422
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.errors.message import ErrorResponse

ns_notes = Namespace(
    name="Sleep diary notes",
    description="Записи из дневника сна",
    path="/",
    decorators=[
        # validate_auth_token,
    ],
)
ns_notes.errorhandler(handler_unprocessable_entity_422)

response_model_400 = response_schema(
    code=HTTP.BAD_REQUEST_400,
    ns=ns_notes,
    model=ErrorResponse,
)
response_model_422 = response_schema(
    code=HTTP.UNPROCESSABLE_ENTITY_422,
    ns=ns_notes,
    model=ErrorResponse,
)
