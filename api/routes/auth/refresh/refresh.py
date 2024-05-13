from flask_restx import Resource

from api.models import User
from api.routes import ns_auth
from api.routes.auth.refresh import response_model_200, response_model_401
from api.routes.edit import response_model_422
from api.utils.auth import get_current_auth_user_for_refresh
from api.utils.jwt import create_access_token, validate_auth_token
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.token import AccessTokenInfo
from common.pydantic_schemas.user import UserValidate


@ns_auth.response(**response_model_200)
@ns_auth.response(**response_model_401)
@ns_auth.response(**response_model_422)
class AuthRefreshJWTRoute(Resource):
    """Обновление Access токена с помощью Refresh токена"""

    @validate_auth_token
    @ns_auth.doc(description=__doc__)
    def post(self) -> tuple:
        current_user: User = get_current_auth_user_for_refresh()
        user: UserValidate = UserValidate.model_validate(current_user)
        access_token: str = create_access_token(user)
        jwt_token: AccessTokenInfo = AccessTokenInfo(access_token=access_token)
        return jwt_token.model_dump(), HTTP.OK_200
