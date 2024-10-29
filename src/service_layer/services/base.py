from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing_extensions import Self

from src.domain.entities import UserEntity


@dataclass
class IUserAuthenticationService(ABC):
    _user: UserEntity = field(init=False)

    @property
    def user(self: Self) -> UserEntity:
        return self._user

    @abstractmethod
    def login(self: Self, username: str, password: str) -> None:
        raise NotImplementedError
