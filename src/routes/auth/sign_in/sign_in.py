from flask import request
from flask_restx import Resource

from src.pydantic_schemas.token import TokenInfo
from src.pydantic_schemas.user import (
    User,
    UserCredentials,
    UserValidate,
)
from src.routes.auth import ns_auth
from src.routes.auth.sign_in import (
    response_model_200,
    response_model_401,
    signin_params,
)
from src.routes.edit import response_model_422
from src.utils.auth import validate_auth_user
from src.utils.jwt import (
    create_access_jwt,
    create_refresh_jwt,
)
from src.utils.status_codes import HTTP


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
        user: User = validate_auth_user(**user_credentials.model_dump())
        user: UserValidate = UserValidate.model_validate(user)
        jwt_token = TokenInfo(
            access_token=create_access_jwt(user),
            refresh_token=create_refresh_jwt(user),
        )
        return jwt_token.model_dump(), HTTP.OK_200
