from flask_restx import Resource

from src.CRUD.user_table import find_user_by_id
from src.models import UserOrm
from src.pydantic_schemas.token import AccessTokenInfo
from src.pydantic_schemas.user import UserValidate
from src.routes import ns_auth
from src.routes.auth.refresh import response_model_200, response_model_401
from src.routes.edit import response_model_422
from src.utils.auth import get_current_auth_user_id_for_refresh
from src.utils.jwt import create_access_jwt, validate_auth_token
from src.utils.status_codes import HTTP


class AuthRefreshJWTRoute(Resource):
    """Обновление Access токена с помощью Refresh токена"""

    @validate_auth_token
    @ns_auth.response(**response_model_200)
    @ns_auth.response(**response_model_401)
    @ns_auth.response(**response_model_422)
    @ns_auth.doc(description=__doc__)
    def post(self) -> tuple:
        current_user_id: int = get_current_auth_user_id_for_refresh()
        db_user: UserOrm = find_user_by_id(current_user_id)
        user: UserValidate = UserValidate.model_validate(db_user)
        access_token: str = create_access_jwt(user)
        jwt_token: AccessTokenInfo = AccessTokenInfo(access_token=access_token)
        return jwt_token.model_dump(), HTTP.OK_200
