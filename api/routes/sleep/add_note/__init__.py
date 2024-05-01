from api.routes.sleep import ns_sleep
from api.schemas.flask_api_models import response_schema
from api.schemas.payload import create_payload_from_model
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNote, SleepNoteModel

response_model_201 = response_schema(
    code=HTTP.CREATED_201,
    ns=ns_sleep,
    model=SleepNoteModel,
)
add_note_payload = create_payload_from_model("json", SleepNote)

from api.routes.sleep.add_note.add_note import AddNoteRoute  # noqa

ns_sleep.add_resource(AddNoteRoute, "/add-note")
