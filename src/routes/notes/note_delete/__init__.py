from src.routes.notes import ns_notes
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP

response_no_content_204 = "Diary note successfully deleted"
response_model_204: dict = response_schema(
    ns=ns_notes,
    code=HTTP.NO_CONTENT_204,
    description=response_no_content_204,
)

note_id_params: dict = {
    "id": {
        "in": "query",
        "description": "Идентификатор записи",
        "required": True,
        "type": "integer",
        "format": "int32",
        "example": "42",
    },
}
