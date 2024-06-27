from flask_restx import Namespace, Resource

from src.exceptions.handlers import handler_unprocessable_entity_422
from src.pydantic_schemas.errors.message import ErrorResponse
from src.utils.jwt import validate_auth_token
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP

ns_notes: Namespace = Namespace(
    name="Sleep diary notes",
    description="Записи из дневника сна",
    path="/note",
    decorators=[validate_auth_token],
)
ns_notes.errorhandler(handler_unprocessable_entity_422)

response_model_400: dict = response_schema(
    code=HTTP.BAD_REQUEST_400,
    ns=ns_notes,
    model=ErrorResponse,
)
response_model_422: dict = response_schema(
    code=HTTP.UNPROCESSABLE_ENTITY_422,
    ns=ns_notes,
    model=ErrorResponse,
)

from src.routes.notes.note_add.note_add import AddNote  # noqa
from src.routes.notes.note_delete.note_delete import DeleteNote  # noqa
from src.routes.notes.note_update.note_update import UpdateNote  # noqa
from src.routes.notes.note_find_by_id.find_by_id import NoteFindById  # noqa
from src.routes.notes.note_find_by_date.find_by_date import NoteFindByDate  # noqa


class NotesRoute(
    Resource,
    AddNote,
    UpdateNote,
    DeleteNote,
):
    ...  # fmt: skip


note_endpoint = "note"
note_find_by_id_endpoint = "note_find_by_id"
note_find_by_date_endpoint = "note_find_by_date"

ns_notes.add_resource(
    NotesRoute,
    "",
    endpoint=note_endpoint,
)

ns_notes.add_resource(
    NoteFindById,
    "/<int:id>",
    endpoint=note_find_by_id_endpoint,
)

ns_notes.add_resource(
    NoteFindByDate,
    "/<string:sleep_date>",
    endpoint=note_find_by_date_endpoint,
)
