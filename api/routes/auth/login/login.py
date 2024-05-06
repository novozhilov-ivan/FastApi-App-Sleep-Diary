from flask import jsonify, request
from flask_restx import Resource

from api.extension import bearer
from api.routes.auth import ns_auth
from api.routes.auth.login import (
    login_params,
    response_model_200,
)
from api.routes.edit import response_model_422
from api.utils.auth import validate_auth_user
from api.utils.jwt import encode_jwt
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.token import TokenInfo
from common.pydantic_schemas.user import CreateUserCredentials


@ns_auth.response(**response_model_200)
@ns_auth.response(**response_model_422)
class AuthUserRoute(Resource):
    """Авторизация в приложении по логину и паролю"""

    @ns_auth.doc(
        description=__doc__,
        security=None,
    )
    @ns_auth.expect(login_params)
    def post(self):
        user_credentials = CreateUserCredentials(**request.form)
        user = validate_auth_user(**user_credentials.model_dump())
        jwt_payload = {
            "sub": user.id,
            "username": user.username,
        }
        encoded_jwt = encode_jwt(jwt_payload)
        jwt_token = TokenInfo(
            access_token=encoded_jwt,
            token_type=bearer,
        )
        response = jsonify(jwt_token.model_dump())
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        response.status_code = HTTP.OK_200
        return response
