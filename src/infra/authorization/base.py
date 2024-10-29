from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any
from typing_extensions import Self
from uuid import uuid4

from jwt import DecodeError, decode, encode

from src.domain.entities.user import UserEntity
from src.infra.authorization.exceptions import (
    JWTAuthorizationException,
    JWTTypeException,
)
from src.project.settings import AuthJWTSettings


TOKEN_TYPE_FIELD: str = "type"


class JWTTypes(StrEnum):
    ACCESS: str = "access"
    REFRESH: str = "refresh"


@dataclass
class BaseTokenService(ABC):
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
        jwt_payload: dict = {TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return self._encode(jwt_payload, expire_timedelta)

    @abstractmethod
    def create_access(self: Self, user: UserEntity) -> dict:
        raise NotImplementedError

    @abstractmethod
    def create_refresh(self: Self, user: UserEntity) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_token_payload(self: Self, credentials: str) -> dict:
        raise NotImplementedError

    @staticmethod
    def _validate_token_type(
        payload: dict[str | JWTTypes, Any],
        token_type: JWTTypes,
    ) -> None:
        current_token_type: JWTTypes | None = payload.get(TOKEN_TYPE_FIELD)

        if current_token_type is None:
            raise JWTAuthorizationException

        if current_token_type != token_type:
            raise JWTTypeException(current_token_type, token_type)
