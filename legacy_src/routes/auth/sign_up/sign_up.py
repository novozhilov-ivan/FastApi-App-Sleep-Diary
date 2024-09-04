from flask import request
from flask_restx import (
    Resource,
    abort,
)

from src.CRUD.user_table import create_new_user_by_username
from src.models import UserOrm
from src.pydantic_schemas.user import UserCredentials
from src.routes import ns_auth
from src.routes.auth.sign_up import (
    response_conflict_409,
    response_created_201,
    response_model_201,
    response_model_409,
    signup_params,
)
from src.routes.edit import response_model_422
from src.utils.auth import hash_password
from src.utils.status_codes import HTTP


class SignUpUserRoute(Resource):
    """
    Регистрация нового пользователя в приложении по имени пользователя и паролю
    """

    @ns_auth.response(**response_model_201)
    @ns_auth.response(**response_model_409)
    @ns_auth.response(**response_model_422)
    @ns_auth.doc(
        description=__doc__,
        security=None,
    )
    @ns_auth.expect(signup_params)
    def post(self) -> tuple:
        user_credentials = UserCredentials(**request.form)
        db_user = UserOrm(
            username=user_credentials.username,
            password=hash_password(user_credentials.password),
        )
        if not create_new_user_by_username(db_user):
            abort(
                code=HTTP.CONFLICT_409,
                message=response_conflict_409,
            )
        return response_created_201, HTTP.CREATED_201
