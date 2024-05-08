from flask import request
from flask_restx import Resource

from api.CRUD.users import create_new_user_by_username
from api.models import User
from api.routes import ns_auth
from api.routes.auth.sign_up import (
    response_created_201,
    response_model_201,
    signup_params,
)
from api.routes.edit import response_model_422
from api.utils.auth import hash_password
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserCredentials


@ns_auth.response(**response_model_201)
@ns_auth.response(**response_model_422)
class SignUpUserRoute(Resource):
    """
    Регистрация нового пользователя в приложении по имени пользователя и паролю
    """

    @ns_auth.doc(
        description=__doc__,
        security=None,
    )
    @ns_auth.expect(signup_params)
    def post(self) -> tuple:
        user_credentials = UserCredentials(**request.form)
        new_user = create_new_user_by_username(
            User(
                login=user_credentials.username,
                password=hash_password(user_credentials.password),
            )
        )
        if not new_user:
            return (
                f"User with username {user_credentials.username!r} "
                f"already exist",
                HTTP.CONFLICT_409,
            )
        return response_created_201, HTTP.CREATED_201
