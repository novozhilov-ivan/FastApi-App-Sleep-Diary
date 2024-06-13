from typing import Callable, Literal

import bcrypt
from flask_restx import abort

from api.CRUD.user_table import read_user_by_username
from api.models import UserOrm
from api.utils.jwt import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    get_current_token_payload,
    validate_token_type,
)
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserCredentials

response_invalid_username_or_password_401 = "invalid username or password"


def hash_password(
    pwd_bytes: bytes,
) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def validate_password(
    password: bytes,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password,
        hashed_password=hashed_password,
    )


def validate_auth_user(
    username: str,
    password: bytes,
) -> UserOrm:
    db_user: UserOrm = read_user_by_username(username)
    if db_user is None:
        abort(
            code=HTTP.UNAUTHORIZED_401,
            message=response_invalid_username_or_password_401,
        )
    user = UserCredentials.model_validate(db_user)
    is_valid_password = validate_password(
        password=password,
        hashed_password=user.password,
    )
    if not is_valid_password:
        abort(
            code=HTTP.UNAUTHORIZED_401,
            message=response_invalid_username_or_password_401,
        )
    return db_user


def get_user_id_by_token_sub(payload: dict) -> int:
    return payload.get("sub")


def get_auth_user_from_token_of_type(
    token_type: str | Literal["access", "refresh"],
) -> Callable:
    def get_current_auth_user_id() -> int:
        payload: dict = get_current_token_payload()
        validate_token_type(payload, token_type)
        current_user = get_user_id_by_token_sub(payload)
        return current_user

    return get_current_auth_user_id


get_current_auth_user_id_for_refresh = get_auth_user_from_token_of_type(
    REFRESH_TOKEN_TYPE,
)
get_current_auth_user_id_for_access = get_auth_user_from_token_of_type(
    ACCESS_TOKEN_TYPE,
)


class UserActions:
    @property
    def current_user_id(self) -> int:
        return get_current_auth_user_id_for_access()
