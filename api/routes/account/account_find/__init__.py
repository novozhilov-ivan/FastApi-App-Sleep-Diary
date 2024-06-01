from api.routes.account import ns_account
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserInfo

response_model_200 = response_schema(
    ns=ns_account,
    model=UserInfo,
    code=HTTP.OK_200,
)

response_not_found_404 = "User not found"
response_model_404 = response_schema(
    ns=ns_account,
    description=response_not_found_404,
    code=HTTP.NOT_FOUND_404,
)
