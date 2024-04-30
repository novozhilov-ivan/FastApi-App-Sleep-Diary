from api.routes import ns_edit

from common.baseclasses.status_codes import HTTP

export_response_created_200 = "Файл со всеми записями дневника сна"
export_response_model_200 = {
    "code": HTTP.OK_200,
    "description": export_response_created_200,
}

from api.routes.edit.export_file.edit_export import EditRouteExport

ns_edit.add_resource(EditRouteExport, "/export")
