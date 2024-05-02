from api.routes import ns_edit
from api.utils.restx_schema import response_schema

from common.baseclasses.status_codes import HTTP

response_no_content_204 = "Все записи из дневника сна удалены"
response_model_204 = response_schema(
    ns=ns_edit,
    code=HTTP.NO_CONTENT_204,
    description=response_no_content_204,
)


from api.routes.edit.delete_diary.edit_delete import EditRouteDelete  # noqa

delete_notes_endpoint = "delete_notes"
ns_edit.add_resource(EditRouteDelete, "/delete", endpoint=delete_notes_endpoint)
