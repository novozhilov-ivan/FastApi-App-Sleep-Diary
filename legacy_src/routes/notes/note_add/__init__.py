from legacy_src.pydantic_schemas.sleep.notes import SleepNote, SleepNoteModel
from legacy_src.routes.notes import ns_notes
from legacy_src.utils.payload import create_payload_from_model
from legacy_src.utils.restx_schema import response_schema
from legacy_src.utils.status_codes import HTTP


response_model_201: dict = response_schema(
    code=HTTP.CREATED_201,
    ns=ns_notes,
    model=SleepNoteModel,
)
add_note_payload: RequestParser = create_payload_from_model(
    location="json",
    model=SleepNote,
)
