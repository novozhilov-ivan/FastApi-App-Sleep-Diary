from functools import wraps

from flask import request
from flask_restx import abort
from jwt import InvalidTokenError

from api.CRUD.users import read_user_by_username
from api.extension import bearer
from api.models import User
from api.utils.jwt import decode_jwt, validate_password
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserValidate

response_invalid_authorization_token_401 = "invalid authorization token"
response_invalid_username_or_password_401 = "invalid username or password"


def validate_auth_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if auth_header is None or bearer not in auth_header:
            abort(
                code=HTTP.UNAUTHORIZED_401,
                message=response_invalid_authorization_token_401,
            )
        *_, token = auth_header.split(" ")
        try:
            decode_jwt(token=token)
        except InvalidTokenError:
            abort(
                code=HTTP.UNAUTHORIZED_401,
                message=response_invalid_authorization_token_401,
            )
        return f(*args, **kwargs)

    return decorated


def validate_auth_user(
    username: str,
    password: bytes,
) -> UserValidate:
    db_user: User = read_user_by_username(username)
    if db_user is None:
        abort(
            code=HTTP.UNAUTHORIZED_401,
            message=response_invalid_username_or_password_401,
        )
    user: UserValidate = UserValidate.model_validate(db_user)
    if not validate_password(
        password=password,
        hashed_password=user.password,
    ):
        abort(
            code=HTTP.UNAUTHORIZED_401,
            message=response_invalid_username_or_password_401,
        )
    return user
