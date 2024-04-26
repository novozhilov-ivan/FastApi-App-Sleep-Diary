from flask_restx import Namespace

from api.exceptions.handlers import handler_not_found_404
from api.schemas.flask_api_models import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.errors.message import ErrorResponse

ns_edit = Namespace(
    name='edit',
    description='Описание edit sleep diary',
    path='/edit',
    validate=True
)
response_model_404 = response_schema(
    ns_edit,
    HTTP.NOT_FOUND_404,
    ErrorResponse
)
response_model_422 = response_schema(
    ns_edit,
    HTTP.UNPROCESSABLE_ENTITY_422,
    ErrorResponse
)
ns_edit.errorhandler(handler_not_found_404)
