from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing_extensions import Self

from src.domain.entities import UserEntity
from src.service_layer.exceptions import NotAuthenticatedException


@dataclass
class NotAuthenticated:
    def __bool__(self: Self) -> bool:
        return False

    def __repr__(self: Self) -> str:
        return "<NotAuthenticated>"


@dataclass
class IUserAuthenticationService(ABC):
    _user: UserEntity | NotAuthenticated = field(
        default_factory=NotAuthenticated,
        init=False,
    )

    @property
    def user(self: Self) -> UserEntity:
        if isinstance(self._user, NotAuthenticated):
            raise NotAuthenticatedException
        return self._user

    @abstractmethod
    def login(self: Self, username: str, password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def logout(self: Self) -> None:
        raise NotImplementedError

    @abstractmethod
    def register(self: Self, username: str, password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def unregister(self: Self) -> None:
        raise NotImplementedError
