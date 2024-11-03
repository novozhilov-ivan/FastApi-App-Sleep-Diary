from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing_extensions import Self

from src.domain.entities import UserEntity
from src.infra.jwt import IPayload, JWTType


@dataclass
class BearerToken:
    token_type: str = field(default="Bearer", init=False)


@dataclass
class AccessToken(BearerToken):
    access_token: str


@dataclass
class RefreshToken(BearerToken):
    refresh_token: str


@dataclass(kw_only=True)
class UserJWTPayload(IPayload):
    sub: str
    username: str

    def convert_to_dict(self: Self) -> dict:
        return {
            "sub": self.sub,
            "username": self.username,
        }


@dataclass
class IUserAuthorizationService(ABC):

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
    def validate_token_type(self: Self, token_type: JWTType) -> None:
        raise NotImplementedError

    @abstractmethod
    def deauthorize(self: Self) -> None:
        raise NotImplementedError
