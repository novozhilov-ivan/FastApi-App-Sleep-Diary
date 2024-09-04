from src.routes.account import ns_account
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP


response_no_content_204 = "Аккаунт удален"
response_model_204: dict = response_schema(
    ns=ns_account,
    description=response_no_content_204,
    code=HTTP.OK_200,
)
