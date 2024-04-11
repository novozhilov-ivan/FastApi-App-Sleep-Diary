from flask_restx import Namespace

from api.exceptions.handler_400 import handler_bad_request_400
from common.baseclasses.status_codes import HTTPStatusCodes

ns_edit = Namespace(
    name='edit',
    description='Описание edit sleep diary',
    path='/edit',
    validate=True
)
# Errors
ns_edit.default_error_handler = handler_bad_request_400

# Get export file
export_response_model_200 = {
        "code": HTTPStatusCodes.STATUS_OK_200,
        "description": 'Файл sleep_diary.csv со всеми записями дневника',
}

from api.routes.edit.edit_export import EditRouteExport
from api.routes.edit.edit_import import EditRouteImport
from api.routes.edit.edit_delete import EditRouteDelete
ns_edit.add_resource(EditRouteExport, '/export')
ns_edit.add_resource(EditRouteExport, '/export')
ns_edit.add_resource(EditRouteImport, '/import')
ns_edit.add_resource(EditRouteDelete, '/delete')
