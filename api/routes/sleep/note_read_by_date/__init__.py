from api.routes import ns_sleep
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.sleep.notes import SleepNote

response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_sleep,
    model=SleepNote,
)
response_not_found_404 = "Note with that calendar date not found"
response_model_404 = response_schema(
    code=HTTP.NOT_FOUND_404,
    ns=ns_sleep,
    description=response_not_found_404,
)
pattern_date = r"^(?:\d{4}-\d{2}-\d{2}\d*)$"

path_params = {
    "calendar_date": {
        "in": "path",
        "description": "Дата записи (YYYY-MM-DD)",
        "required": True,
        "type": "string",
        "format": "date",
        "example": "2021-12-13",
        "pattern": pattern_date,
    },
}

note_read_by_date_endpoint = "/note/date"

from api.routes.sleep.note_read_by_date.note_read_by_date import (
    NoteReadByDateRoute,
)  # noqa

ns_sleep.add_resource(
    NoteReadByDateRoute,
    f"{note_read_by_date_endpoint}/<string:calendar_date>",
    endpoint=note_read_by_date_endpoint,
)
