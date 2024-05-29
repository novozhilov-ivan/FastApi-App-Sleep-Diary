from api.routes.account import ns_account
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP

response_no_content_204 = "Аккаунт удален"
response_model_204 = response_schema(
    ns=ns_account,
    description=response_no_content_204,
    code=HTTP.OK_200,
)
