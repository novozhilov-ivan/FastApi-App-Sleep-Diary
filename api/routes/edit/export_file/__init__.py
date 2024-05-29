from api.routes import ns_edit
from api.utils.restx_schema import response_schema

from common.baseclasses.status_codes import HTTP

response_ok_200 = "Файл со всеми записями дневника сна"
response_model_200 = response_schema(
    ns=ns_edit,
    code=HTTP.OK_200,
    description=response_ok_200,
)

from api.routes.edit.export_file.edit_export import EditRouteExport  # noqa

export_notes_endpoint = "export_notes"
ns_edit.add_resource(
    EditRouteExport,
    "/export",
    endpoint=export_notes_endpoint,
)
