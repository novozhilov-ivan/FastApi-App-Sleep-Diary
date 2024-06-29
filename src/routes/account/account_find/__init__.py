from src.pydantic_schemas.user import UserInfo
from src.routes.account import ns_account
from src.utils.restx_schema import response_schema
from src.utils.status_codes import HTTP


response_model_200: dict = response_schema(
    ns=ns_account,
    model=UserInfo,
    code=HTTP.OK_200,
)

response_not_found_404 = "User not found"
response_model_404: dict = response_schema(
    ns=ns_account,
    description=response_not_found_404,
    code=HTTP.NOT_FOUND_404,
)
