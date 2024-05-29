from flask import request
from flask_restx import Resource

from api.routes.auth import ns_auth
from api.routes.auth.sign_in import (
    response_model_200,
    response_model_401,
    signin_params,
)
from api.routes.edit import response_model_422
from api.utils.auth import validate_auth_user
from api.utils.jwt import create_access_token, create_refresh_token
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.token import TokenInfo
from common.pydantic_schemas.user import UserCredentials, UserValidate


class AuthUserRoute(Resource):
    """Авторизация в приложении по логину и паролю"""

    @ns_auth.response(**response_model_200)
    @ns_auth.response(**response_model_401)
    @ns_auth.response(**response_model_422)
    @ns_auth.doc(
        description=__doc__,
        security=None,
    )
    @ns_auth.expect(signin_params)
    def post(self) -> tuple:
        user_credentials = UserCredentials(**request.form)
        user = validate_auth_user(
            username=user_credentials.username,
            password=user_credentials.password,
        )
        user = UserValidate.model_validate(user)
        access_token: str = create_access_token(user)
        refresh_token: str = create_refresh_token(user)
        jwt_token = TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token,
        )
        return jwt_token.model_dump(), HTTP.OK_200
