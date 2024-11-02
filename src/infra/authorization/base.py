from abc import ABC, abstractmethod
from dataclasses import InitVar, dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing_extensions import Self
from uuid import uuid4

from src.domain.entities import UserEntity
from src.infra.authorization.exceptions import JWTExpireAtFieldException


class TokenType(StrEnum):
    ACCESS: str = "access"
    REFRESH: str = "refresh"


@dataclass
class BearerToken:
    token_type: str = field(default="Bearer", init=False)


@dataclass
class AccessToken(BearerToken):
    access_token: str


@dataclass
class RefreshToken(BearerToken):
    refresh_token: str


@dataclass
class IPayload(ABC):
    @abstractmethod
    def convert_to_dict(self: Self) -> dict:
        raise NotImplementedError


@dataclass(kw_only=True)
class JWTPayload(IPayload):
    typ: TokenType

    expire_timedelta: InitVar[timedelta | None] = None

    iat: float = field(
        default_factory=lambda: datetime.now(UTC).timestamp(),
    )
    exp: float | None = None
    jti: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self: Self, expire_timedelta: timedelta | None) -> None:
        if self.exp is None and expire_timedelta is None:
            raise JWTExpireAtFieldException

        if expire_timedelta is not None:
            self.exp = self.iat + expire_timedelta.seconds

    def convert_to_dict(self: Self) -> dict:
        return {
            "type_": self.typ.value,
            "iat": self.iat,
            "exp": self.exp,
            "jti": self.jti,
        }


@dataclass(kw_only=True)
class UserJWTPayload(JWTPayload, IPayload):
    sub: str
    username: str

    def convert_to_dict(self: Self) -> dict:
        return {
            "sub": self.sub,
            "username": self.username,
            **super().convert_to_dict(),
        }


@dataclass
class IUserTokenService(ABC):

    @abstractmethod
    def create_access(self: Self, user: UserEntity) -> AccessToken:
        raise NotImplementedError

    @abstractmethod
    def create_refresh(self: Self, user: UserEntity) -> RefreshToken:
        raise NotImplementedError

    @abstractmethod
    def get_payload(self: Self, token: str) -> UserJWTPayload:
        raise NotImplementedError

    @abstractmethod
    def validate_token_type(self: Self, token_type: TokenType) -> None:
        raise NotImplementedError

    @abstractmethod
    def deauthorize(self: Self) -> None:
        raise NotImplementedError
