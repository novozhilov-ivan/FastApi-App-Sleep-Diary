from flask import request
from flask_restx import Resource

from api.routes.auth import ns_auth
from api.routes.auth.login import (
    login_params,
    response_model_200,
    response_model_401,
)
from api.routes.edit import response_model_422
from api.utils.auth import validate_auth_user
from api.utils.jwt import encode_jwt
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.token import TokenInfo
from common.pydantic_schemas.user import CreateUserCredentials


@ns_auth.response(**response_model_200)
@ns_auth.response(**response_model_401)
@ns_auth.response(**response_model_422)
class AuthUserIssueJWTRoute(Resource):
    """Авторизация в приложении по логину и паролю"""

    @ns_auth.doc(description=__doc__)
    @ns_auth.expect(login_params)
    def post(self):
        user_credentials = CreateUserCredentials(**request.form)
        user = validate_auth_user(**user_credentials.model_dump())
        jwt_payload = {
            "sub": user.id,
            "username": user.username,
        }
        token = encode_jwt(jwt_payload)
        token = TokenInfo(
            access_token=token,
            token_type="Bearer",
        )
        return token.model_dump(), HTTP.OK_200
