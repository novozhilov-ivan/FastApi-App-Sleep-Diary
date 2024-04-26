from api.schemas.payload import create_payload
from common.baseclasses.status_codes import HTTP

allowed_file_extensions = ('csv',)
import_file_payload = create_payload(
    name='file',
    type_='file',
    required=True,
    description=f'Файл формата {", ".join(allowed_file_extensions)} с записями дневника сна',
    location='files'
)
import_response_created_201 = "Все импортированные записи созданы"
import_response_model_201 = {
    "code": HTTP.CREATED_201,
    "description": import_response_created_201,
}
import_response_bad_request_400 = 'Not payload'
import_response_model_400 = {
    "code": HTTP.BAD_REQUEST_400,
    "description": import_response_bad_request_400,
}
import_response_unsupported_media_type_415 = 'File extension not allowed'
import_response_model_415 = {
    "code": HTTP.UNSUPPORTED_MEDIA_TYPE_415,
    "description": import_response_unsupported_media_type_415,
}
import_response_conflict_409 = 'Some sleep notes in file already exists. Date of note must be unique!'
import_response_model_409 = {
    "code": HTTP.CONFLICT_409,
    "description": import_response_conflict_409,
}
import_response_content_too_large_413 = "Content length too large"
import_response_model_413 = {
    "code": HTTP.CONTENT_TOO_LARGE_413,
    "description": import_response_content_too_large_413,
}

from api.routes.edit.import_file.edit_import import EditRouteImport, ns_edit

ns_edit.add_resource(EditRouteImport, '/import')
