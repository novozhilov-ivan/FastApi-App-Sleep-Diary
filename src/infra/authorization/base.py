from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing_extensions import Self

from src.domain.entities import UserEntity
from src.infra.authorization.payloads import (
    AccessToken,
    RefreshToken,
    UserJWTPayload,
)
from src.infra.jwt import JWTType


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
