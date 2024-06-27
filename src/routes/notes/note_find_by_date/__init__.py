from src.pydantic_schemas.sleep.notes import SleepNote
from src.routes.notes import ns_notes
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP

response_model_200: dict = response_schema(
    code=HTTP.OK_200,
    ns=ns_notes,
    model=SleepNote,
)
response_not_found_404 = "Note with that calendar date not found"
response_model_404: dict = response_schema(
    code=HTTP.NOT_FOUND_404,
    ns=ns_notes,
    description=response_not_found_404,
)
pattern_date = r"^(?:\d{4}-\d{2}-\d{2}\d*)$"

path_params: dict = {
    "sleep_date": {
        "in": "path",
        "description": "Дата записи (YYYY-MM-DD)",
        "required": True,
        "type": "string",
        "format": "date",
        "example": "2021-12-13",
        "pattern": pattern_date,
    },
}
