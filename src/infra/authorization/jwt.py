from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any, ClassVar, cast
from typing_extensions import Self
from uuid import uuid4

from jwt import DecodeError, decode, encode

from src.domain.entities import UserEntity
from src.infra.authorization.base import IUserTokenService
from src.infra.authorization.exceptions import (
    JWTAuthorizationException,
    JWTTypeException,
)
from src.project.settings import AuthJWTSettings


class JWTTypes(StrEnum):
    ACCESS: str = "access"
    REFRESH: str = "refresh"


@dataclass
class UserJWTService(IUserTokenService):
    TOKEN_TYPE_FIELD: ClassVar[str] = "type"

    settings: AuthJWTSettings

    def _encode(
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

    def _decode(self: Self, token: str | bytes) -> dict:
        try:
            return decode(
                jwt=token,
                key=self.settings.PUBLIC_KEY,
                algorithms=[self.settings.ALGORITHM],
            )
        except DecodeError:
            raise JWTAuthorizationException

    def _create(
        self: Self,
        token_type: JWTTypes,
        token_data: dict[str, Any],
        expire_timedelta: timedelta | None = None,
    ) -> str:
        jwt_payload: dict = {self.TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return self._encode(jwt_payload, expire_timedelta)

    def create_access(self: Self, user: UserEntity) -> dict:
        jwt_payload = {
            "sub": user.oid,
            "username": user.username,
        }

        return {
            "access_token": self._create(
                token_type=JWTTypes.ACCESS,
                token_data=jwt_payload,
            ),
        }

    def create_refresh(self: Self, user: UserEntity) -> dict:
        payload = {
            "sub": user.oid,
            "username": user.username,
        }
        expire_timedelta = timedelta(days=self.settings.REFRESH_TOKEN_EXPIRE_DAYS)

        return {
            "refresh_token": self._create(
                token_type=JWTTypes.REFRESH,
                token_data=payload,
                expire_timedelta=expire_timedelta,
            ),
        }

    def get_token_payload(self: Self, credentials: str) -> dict:
        return self._decode(credentials)

    @staticmethod
    def _validate_token_type(
        payload: dict[str, Any],
        token_type: JWTTypes,
    ) -> None:
        current_token_type: JWTTypes | None = payload.get(
            UserJWTService.TOKEN_TYPE_FIELD,
        )

        if current_token_type is None:
            raise JWTAuthorizationException

        cast(JWTTypes, current_token_type)
        if current_token_type != token_type:
            raise JWTTypeException(current_token_type, token_type)

    # def validate_authentication_token():
    #     auth_header: str | None = request.headers.get("Authorization")
    #
    #     if auth_header is None or bearer not in auth_header:
    #         abort(
    #             code=HTTP.UNAUTHORIZED_401,
    #             message=response_invalid_authorization_token_401,
    #         )
    #     *_, token = auth_header.split(" ")
    #     decode_jwt(token=token)
    #
    #     return decorated

    # def get_current_token_payload(
    #     self: Self,
    #     credentials=Headers("Authorization"),
    # ) -> dict:
    #     *_, token = credentials.split(" ")
    #     return self.decode_jwt(token=token)
    #
    # @staticmethod
    # def get_user_oid_by_token_sub(payload: dict) -> UUID:
    #     return payload.get("sub")
    #
    # def get_auth_user_from_token_of_type(
    #     self: Self,
    #     token_type: JWTTypes,
    # ) -> Callable:
    #     def get_current_auth_user_id() -> int:
    #         payload: dict = get_current_token_payload()
    #         validate_token_type(payload, token_type)
    #         current_user = get_user_id_by_token_sub(payload)
    #         return current_user
    #
    #     return get_current_auth_user_id
    #
    # get_current_auth_user_id_for_refresh = get_auth_user_from_token_of_type(
    #     token_type=JWTTypes.REFRESH,
    # )
    # get_current_auth_user_id_for_access = get_auth_user_from_token_of_type(
    #     token_type=JWTTypes.ACCESS,
    # )


# class UserActions:
#     @property
#     def current_user_id(self) -> int:
#         return get_current_auth_user_id_for_access()
