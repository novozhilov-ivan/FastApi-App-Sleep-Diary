from api.routes import ns_edit
from api.schemas.flask_api_models import response_schema
from api.schemas.payload import create_payload
from common.baseclasses.status_codes import HTTP

allowed_file_extensions = ("csv",)
import_file_payload = create_payload(
    name="file",
    type_="file",
    required=True,
    description=f"Файл формата {', '.join(allowed_file_extensions)} с "
    f"записями дневника сна",
    location="files",
)
response_created_201 = "Все импортированные записи созданы"
response_model_201 = response_schema(
    ns=ns_edit,
    code=HTTP.CREATED_201,
    description=response_created_201,
)
response_bad_request_400 = "Not payload"
response_model_400 = response_schema(
    ns=ns_edit,
    code=HTTP.BAD_REQUEST_400,
    description=response_bad_request_400,
)
response_unsupported_media_type_415 = "File extension not allowed"
response_model_415 = response_schema(
    ns=ns_edit,
    code=HTTP.UNSUPPORTED_MEDIA_TYPE_415,
    description=response_unsupported_media_type_415,
)
response_conflict_409 = (
    "Some sleep notes from file already exists. Date of note must be unique!"
)
response_model_409 = response_schema(
    ns=ns_edit,
    code=HTTP.CONFLICT_409,
    description=response_conflict_409,
)
response_content_too_large_413 = "Content length too large"
response_model_413 = response_schema(
    ns=ns_edit,
    code=HTTP.CONTENT_TOO_LARGE_413,
    description=response_content_too_large_413,
)

from api.routes.edit.import_file.edit_import import EditRouteImport  # noqa

ns_edit.add_resource(EditRouteImport, "/import")
