from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any
from typing_extensions import Self
from uuid import uuid4

from jwt import InvalidTokenError, decode, encode

from src.infrastructure.authentication.schema import UserValidate
from src.project.settings import AuthJWTSettings


TOKEN_TYPE_FIELD: str = "type"


class JWTTokenTypes(StrEnum):
    ACCESS_TOKEN_TYPE: str = "access"
    REFRESH_TOKEN_TYPE: str = "refresh"


@dataclass
class JWTAuthorizationService:
    settings: AuthJWTSettings

    def encode_jwt(
        self: Self,
        payload: dict,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        to_encode = payload.copy()
        utc_now = datetime.now(UTC)

        if expire_timedelta is not None:
            expire = utc_now + expire_timedelta
        else:
            expire = utc_now + timedelta(
                minutes=self.settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            )

        to_encode.update(exp=expire, iat=utc_now, jti=str(uuid4()))

        return encode(
            payload=to_encode,
            key=self.settings.PRIVATE_KEY,
            algorithm=self.settings.ALGORITHM,
        )

    def decode_jwt(self: Self, token: str | bytes) -> dict:
        try:
            return decode(
                jwt=token,
                key=self.settings.PUBLIC_KEY,
                algorithms=[self.settings.ALGORITHM],
            )
            # TODO сделать без try; те возбудить и отловить потом либо
        except InvalidTokenError:
            # TODO обработать
            raise JWTTokenException(response_invalid_authorization_token_401)

    def create_jwt(
        self: Self,
        token_type: JWTTokenTypes,
        token_data: dict[str, Any],
        expire_timedelta: timedelta | None = None,
    ) -> str:
        jwt_payload: dict = {TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return self.encode_jwt(jwt_payload, expire_timedelta)

    def create_access_jwt(self: Self, user: UserValidate) -> str:
        jwt_payload = {
            "sub": user.oid,
            "username": user.username,
        }

        return self.create_jwt(
            token_type=JWTTokenTypes.ACCESS_TOKEN_TYPE,
            token_data=jwt_payload,
        )

    def create_refresh_jwt(self: Self, user: UserValidate) -> str:
        jwt_payload = {
            "sub": user.oid,
            "username": user.username,
        }
        expire_timedelta = timedelta(days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS)

        return self.create_jwt(
            token_type=JWTTokenTypes.REFRESH_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_timedelta=expire_timedelta,
        )

    @staticmethod
    def validate_token_type(
        payload: dict,
        token_type: JWTTokenTypes,
    ) -> None:
        current_token_type = payload.get(TOKEN_TYPE_FIELD)

        if current_token_type != token_type:
            # TODO Обработать
            raise JWTTokenException(
                response_invalid_token_type_401.format(
                    f"{current_token_type!r}",
                    f"{token_type!r}",
                ),
            )


#     def validate_authentication_token():
#         auth_header: str | None = request.headers.get("Authorization")
#
#         if auth_header is None or bearer not in auth_header:
#             abort(
#                 code=HTTP.UNAUTHORIZED_401,
#                 message=response_invalid_authorization_token_401,
#             )
#         *_, token = auth_header.split(" ")
#         decode_jwt(token=token)
#
#         return decorated
#
#     def get_current_token_payload(self: Self) -> dict:
#         credentials = request.headers.get("Authorization")
#         *_, token = credentials.split(" ")
#         return self.decode_jwt(token=token)
#
#     @staticmethod
#     def get_user_oid_by_token_sub(payload: dict) -> UUID:
#         return payload.get("sub")
#
#     def get_auth_user_from_token_of_type(
#         token_type: str | Literal["access", "refresh"],
#     ) -> Callable:
#         def get_current_auth_user_id() -> int:
#             payload: dict = get_current_token_payload()
#             validate_token_type(payload, token_type)
#             current_user = get_user_id_by_token_sub(payload)
#             return current_user
#
#         return get_current_auth_user_id
#
#     get_current_auth_user_id_for_refresh = get_auth_user_from_token_of_type(
#         token_type=JWTTokenTypes.REFRESH_TOKEN_TYPE,
#     )
#     get_current_auth_user_id_for_access = get_auth_user_from_token_of_type(
#         token_type=JWTTokenTypes.ACCESS_TOKEN_TYPE,
#     )
#
#
# class UserActions:
#     @property
#     def current_user_id(self) -> int:
#         return get_current_auth_user_id_for_access()
