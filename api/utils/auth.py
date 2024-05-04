from functools import wraps

from flask import request

from api.CRUD.users import read_user_by_username
from api.extension import bearer
from api.models import User
from api.routes.auth.login import response_invalid_user_or_password_401
from api.utils.jwt import validate_password
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserValidate

response_invalid_token_error_401 = "invalid token"


def validate_auth_user(
    username: str,
    password: bytes,
):
    unauthorized_exc: tuple = (
        response_invalid_user_or_password_401,
        HTTP.UNAUTHORIZED_401,
    )
    db_user: User = read_user_by_username(username)
    if not db_user:
        return unauthorized_exc
    user = UserValidate.model_validate(db_user)
    if not validate_password(
        password=password,
        hashed_password=user.password,
    ):
        return unauthorized_exc
    return user


response_invalid_auth_header_401 = "invalid authorization header"


def validate_auth_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if auth_header is None or bearer not in auth_header:
            return response_invalid_auth_header_401, HTTP.UNAUTHORIZED_401

        auth_schema, credentials = auth_header.split(" ")

        # TODO прикрутить валидацию тут
        # TODO Зарефакторить return'ы с ошибками, сделать abort()
        # Здесь должна быть логика проверки и дешифрации токена
        # Например, использование JWT для верификации токена
        return f(*args, **kwargs)

    return decorated
