from api.CRUD.users import read_user_by_username
from api.models import User
from api.routes.auth.login import response_unauthorized_401
from api.utils.jwt import validate_password
from common.baseclasses.status_codes import HTTP
from common.pydantic_schemas.user import UserSchema


def validate_auth_user(
    username: str,
    password: bytes,
):
    unauthorized_exc: tuple = (
        response_unauthorized_401,
        HTTP.UNAUTHORIZED_401,
    )
    db_user: User = read_user_by_username(username)
    if not db_user:
        return unauthorized_exc
    user = UserSchema.model_validate(db_user)
    if not validate_password(
        password=password,
        hashed_password=user.password,
    ):
        return unauthorized_exc
    return user
