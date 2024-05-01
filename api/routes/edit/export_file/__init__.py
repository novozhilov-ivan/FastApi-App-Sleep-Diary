from api.routes import ns_edit
from api.schemas.flask_api_models import response_schema

from common.baseclasses.status_codes import HTTP

response_ok_200 = "Файл со всеми записями дневника сна"
response_model_200 = response_schema(
    ns=ns_edit,
    code=HTTP.OK_200,
    description=response_ok_200,
)

from api.routes.edit.export_file.edit_export import EditRouteExport  # noqa

ns_edit.add_resource(EditRouteExport, "/export")
