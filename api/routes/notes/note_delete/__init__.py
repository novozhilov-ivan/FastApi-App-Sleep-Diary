from api.routes.notes import ns_notes
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP

response_no_content_204 = "Diary note successfully deleted"
response_model_204 = response_schema(
    ns=ns_notes,
    code=HTTP.NO_CONTENT_204,
    description=response_no_content_204,
)

note_id_params = {
    "note_id": {
        "in": "query",
        "description": "ID записи",
        "required": True,
        "type": "integer",
        "format": "int32",
        "example": "42",
    },
}
