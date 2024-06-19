from pydantic import ValidationError

from src.extension import api
from src.pydantic_schemas.errors.message import ErrorResponse
from src.utils.status_codes import HTTP


@api.errorhandler(ValidationError)
def handler_bad_request_400(error: ValidationError):
    status = HTTP.BAD_REQUEST_400
    response = ErrorResponse(
        errors_count=error.error_count(),
        message=error.errors(),
    )
    response = response.model_dump()
    return response, status


@api.errorhandler(ValidationError)
def handler_unprocessable_entity_422(error: ValidationError):
    status = HTTP.UNPROCESSABLE_ENTITY_422
    response = ErrorResponse(
        errors_count=error.error_count(),
        message=error.errors(),
    )
    response = response.model_dump()
    return response, status
