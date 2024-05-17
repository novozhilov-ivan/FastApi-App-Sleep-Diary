from api.routes.notes import ns_notes
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP

response_no_content_204 = "Diary note successfully updated"
response_model_204 = response_schema(
    code=HTTP.NO_CONTENT_204,
    ns=ns_notes,
    description=response_no_content_204,
)
