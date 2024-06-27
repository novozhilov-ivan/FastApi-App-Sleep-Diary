from src.routes import ns_edit
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP

response_no_content_204 = "Все записи из дневника сна удалены"
response_model_204: dict = response_schema(
    ns=ns_edit,
    code=HTTP.NO_CONTENT_204,
    description=response_no_content_204,
)

from src.routes.edit.delete_diary.edit_delete import EditRouteDelete  # noqa

delete_notes_endpoint = "delete_notes"
ns_edit.add_resource(
    EditRouteDelete,
    "/delete",
    endpoint=delete_notes_endpoint,
)
