from api.routes import ns_edit

from api.schemas.flask_api_models import response_schema
from common.baseclasses.status_codes import HTTPStatusCodes
from common.pydantic_schemas.errors.message import ErrorResponse

export_response_model_200 = {
    "code": HTTPStatusCodes.STATUS_OK_200,
    "description": 'Файл со всеми записями дневника сна',
}
export_response_model_404 = response_schema(
    ns_edit,
    HTTPStatusCodes.STATUS_NOT_FOUND_404,
    ErrorResponse
)

from api.routes.edit.export_file.edit_export import EditRouteExport

ns_edit.add_resource(EditRouteExport, '/export')
