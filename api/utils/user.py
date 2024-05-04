from api.CRUD.users import read_user_by_id
from api.models import User
from api.utils.jwt import decode_jwt


def get_current_token_payload(credentials: str) -> dict:
    *_, token = credentials.split(" ")
    payload = decode_jwt(
        token=token,
    )
    return payload


def get_current_auth_user(payload: dict) -> User:
    user_id = payload.get("sub")
    return read_user_by_id(user_id)
