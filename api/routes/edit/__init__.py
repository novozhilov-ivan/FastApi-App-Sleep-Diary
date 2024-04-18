from flask_restx import Namespace

from api.exceptions.handlers import handler_not_found_404
from api.schemas.flask_api_models import response_schema
from api.schemas.payload import create_payload
from common.baseclasses.status_codes import HTTPStatusCodes
from common.pydantic_schemas.errors.message import ErrorResponse
from common.pydantic_schemas.sleep.notes import ListWithSleepNotes

ns_edit = Namespace(
    name='edit',
    description='Описание edit sleep diary',
    path='/edit',
    validate=True
)
ns_edit.errorhandler(handler_not_found_404)
# Get export file
export_response_model_200 = {
    "code": HTTPStatusCodes.STATUS_OK_200,
    "description": 'Файл со всеми записями дневника сна',
}
export_response_model_404 = response_schema(
    ns_edit,
    HTTPStatusCodes.STATUS_NOT_FOUND_404,
    ErrorResponse
)
file_ext_allowed = ('csv',)
import_file_payload = create_payload(
    name='file',
    type_='file',
    required=True,
    description=f'Файл формата {", ".join(file_ext_allowed)} с записями дневника сна',
    location='files'
)

import_response_model_201 = response_schema(
    code=HTTPStatusCodes.STATUS_CREATED_201,
    ns=ns_edit,
    model=ListWithSleepNotes,
    description='Успешно импортированные в дневник записи'
)

from api.routes.edit.edit_export import EditRouteExport
from api.routes.edit.edit_import import EditRouteImport
from api.routes.edit.edit_delete import EditRouteDelete

ns_edit.add_resource(EditRouteExport, '/export')
ns_edit.add_resource(EditRouteImport, '/import')
ns_edit.add_resource(EditRouteDelete, '/delete')
