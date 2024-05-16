from datetime import date
from enum import Enum

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
response_unprocessable_entity_422 = (
    "Value must keep format 'YYYY-MM-DD' or an " "integer and a positive number"
)
response_model_422 = response_schema(
    code=HTTP.UNPROCESSABLE_ENTITY_422,
    ns=ns_sleep,
    description=response_unprocessable_entity_422,
)
pattern_date_or_int = r"^(?:\d{4}-\d{2}-\d{2}|[1-9]\d*)$"
pattern_date = r"^(?:\d{4}-\d{2}-\d{2}\d*)$"


class ParamsDateOrInt(Enum):
    """Дата записи (YYYY-MM-DD) или ID записи"""

    calendar_date: date = "calendar_date"
    note_id: int = "note_id"


params = tuple(e.value for e in ParamsDateOrInt)

path_params = {
    "choice": {
        "in": "path",
        "type": "string",
        "format": "string",
        "description": "Тип поиска записи, по дате ('calendar_date') или "
        "по ID ('note_id')",
        "required": True,
        "enum": params,
    },
    "value": {
        "in": "path",
        "required": True,
        "description": ParamsDateOrInt.__doc__,
        "example": ", ".join(["2021-12-13", "42"]),
        "type": "string",
        "pattern": pattern_date_or_int,
    },
}

from api.routes.sleep.note_read.note_read import NoteReadRoute  # noqa

note_read_endpoint = "/note"
ns_sleep.add_resource(
    NoteReadRoute,
    f"{note_read_endpoint}/<any({', '.join(params)}):choice>/<string:value>",
    endpoint=note_read_endpoint,
)
