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

from api.routes.sleep.note_read.note_read import NoteReadRoute  # noqa

note_read_endpoint = "/note"
ns_sleep.add_resource(
    NoteReadRoute,
    f"{note_read_endpoint}/<string:calendar_date>/",
    endpoint=note_read_endpoint,
)
