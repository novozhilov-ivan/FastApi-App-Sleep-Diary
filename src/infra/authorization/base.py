from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing_extensions import Self

from src.domain.entities import UserEntity


@dataclass
class IUserTokenService(ABC):

    @abstractmethod
    def create_access(self: Self, user: UserEntity) -> dict:
        raise NotImplementedError

    @abstractmethod
    def create_refresh(self: Self, user: UserEntity) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_token_payload(self: Self, credentials: str) -> dict:
        raise NotImplementedError
