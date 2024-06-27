from flask_restx.reqparse import RequestParser

from src.pydantic_schemas.sleep.notes import SleepNote, SleepNoteModel
from src.routes.notes import ns_notes
from src.utils.payload import create_payload_from_model
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP

response_model_201: dict = response_schema(
    code=HTTP.CREATED_201,
    ns=ns_notes,
    model=SleepNoteModel,
)
add_note_payload: RequestParser = create_payload_from_model(
    location="json",
    model=SleepNote,
)
