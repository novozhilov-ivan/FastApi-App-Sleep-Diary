from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing_extensions import Self

from src.domain.entities import UserEntity
from src.infra.jwt import IPayload, JWTPayload, JWTType


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
class UserPayload(IPayload):
    sub: str
    username: str

    def convert_to_dict(self: Self) -> dict:
        return {
            "sub": self.sub,
            "username": self.username,
        }


@dataclass(kw_only=True)
class UserJWTPayload(JWTPayload, UserPayload):
    pass


@dataclass
class IUserJWTAuthorizationService(ABC):

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
    def validate_token_type(self: Self, jwt_type: JWTType) -> None:
        raise NotImplementedError

    @abstractmethod
    def deauthorize(self: Self) -> None:
        raise NotImplementedError
