from api.routes import ns_edit

from common.baseclasses.status_codes import HTTP

delete_response_ok_200 = "Все записи из дневника сна удалены"
delete_response_model_200 = {
    "code": HTTP.OK_200,
    "description": delete_response_ok_200,
}

from api.routes.edit.delete_diary.edit_delete import EditRouteDelete

ns_edit.add_resource(EditRouteDelete, '/delete')
