from api.routes.notes import ns_notes
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP

response_ok_200 = "Diary note successfully updated"
response_model_200 = response_schema(
    code=HTTP.OK_200,
    ns=ns_notes,
    description=response_ok_200,
)
