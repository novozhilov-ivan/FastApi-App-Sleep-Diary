# from api.routes import ns_edit
from api.schemas.payload import create_payload
from common.baseclasses.status_codes import HTTPStatusCodes

allowed_file_extensions = ('csv',)
import_file_payload = create_payload(
    name='file',
    type_='file',
    required=True,
    description=f'Файл формата {", ".join(allowed_file_extensions)} с записями дневника сна',
    location='files'
)
import_success_response = "Все импортированные записи созданы"
import_response_model_201 = {
    "code": HTTPStatusCodes.STATUS_CREATED_201,
    "description": import_success_response,
}

from api.routes.edit.import_file.edit_import import EditRouteImport, ns_edit

ns_edit.add_resource(EditRouteImport, '/import')
