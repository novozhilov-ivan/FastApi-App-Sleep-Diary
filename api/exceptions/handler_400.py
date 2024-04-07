from pydantic import ValidationError

from api import api


@api.errorhandler(ValidationError)
def handler_bad_request(error: ValidationError):
    status = 400
    response = {
        'errors_count': error.error_count(),
        'message': error.errors(
            include_input=False,
            include_context=False,
            include_url=False
        )
    }
    return response, status
