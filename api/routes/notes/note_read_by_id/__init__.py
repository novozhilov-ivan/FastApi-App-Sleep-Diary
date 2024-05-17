from api.routes.notes import ns_notes
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNote

response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_notes,
    model=SleepNote,
)
response_not_found_404 = "Note with that id not found"
response_model_404 = response_schema(
    code=HTTP.NOT_FOUND_404,
    ns=ns_notes,
    description=response_not_found_404,
)

path_params = {
    "note_id": {
        "in": "path",
        "description": "ID записи",
        "required": True,
        "type": "integer",
        "format": "int32",
        "example": "42",
    },
}
note_read_by_id_endpoint = "/note"

from api.routes.notes.note_read_by_id.note_read_by_id import (
    NoteReadByIdRoute,
    # noqa
)

ns_notes.add_resource(
    NoteReadByIdRoute,
    f"{note_read_by_id_endpoint}/<int:note_id>",
    endpoint=note_read_by_id_endpoint,
)
