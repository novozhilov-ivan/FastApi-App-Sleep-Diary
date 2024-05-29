from api.routes.account import ns_account
from api.utils.restx_schema import response_schema
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserInfo

response_model_200 = response_schema(
    ns=ns_account,
    model=UserInfo,
    code=HTTP.OK_200,
)
