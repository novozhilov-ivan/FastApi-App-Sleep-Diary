from api.routes.notes import ns_notes
from api.utils.payload import create_payload_from_model
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNote, SleepNoteModel

response_model_201 = response_schema(
    code=HTTP.CREATED_201,
    ns=ns_notes,
    model=SleepNoteModel,
)
add_note_payload = create_payload_from_model("json", SleepNote)

from api.routes.notes.note_add.note_add import AddNoteRoute  # noqa

note_add_endpoint = "/note/add"
ns_notes.add_resource(
    AddNoteRoute,
    note_add_endpoint,
    endpoint=note_add_endpoint,
)
