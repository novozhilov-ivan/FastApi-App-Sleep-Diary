from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar, Self

from bcrypt import checkpw, gensalt, hashpw

from src.sleep_diary.application.exceptions import (
    LogInException,
    UserCredentialsFormatException,
    UserNameAlreadyExistException,
)
from src.sleep_diary.domain.entities import UserEntity
from src.sleep_diary.domain.services import IUsersRepository
from src.sleep_diary.domain.specifications import (
    UserCredentialsSpecification,
)


@dataclass
class IUserAuthenticationService(ABC):
    @abstractmethod
    def login(self: Self, username: str, password: str) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    def register(self: Self, username: str, password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def unregister(self: Self) -> None:
        raise NotImplementedError


@dataclass
class UserAuthenticationService(IUserAuthenticationService):
    _DEFAULT_ENCODING: ClassVar[str] = "utf-8"

    repository: IUsersRepository

    def login(self: Self, username: str, password: str) -> UserEntity:
        if (user := self.repository.get_by_username(username)) is None:
            raise LogInException

        self._validate_user_password(user, password)

        return user

    def register(self: Self, username: str, password: str) -> None:
        if self.repository.get_by_username(username) is not None:
            raise UserNameAlreadyExistException

        if not (specification := UserCredentialsSpecification(username, password)):
            raise UserCredentialsFormatException(specification)

        self.repository.add_user(
            UserEntity(
                username=username,
                password=self.hash_password(password),
            ),
        )

    def unregister(self: Self) -> None:
        self.repository.delete_user(self.user.username)
        self.logout()

    @staticmethod
    def hash_password(pwd: str, encoding: str = _DEFAULT_ENCODING) -> str:
        return hashpw(
            password=pwd.encode(encoding),
            salt=gensalt(),
        ).decode(encoding)

    @staticmethod
    def compare_passwords(
        password: str,
        hashed_password: str,
        encoding: str = _DEFAULT_ENCODING,
    ) -> bool:
        return checkpw(
            password=password.encode(encoding),
            hashed_password=hashed_password.encode(encoding),
        )

    def _validate_user_password(self: Self, user: UserEntity, password: str) -> None:
        if not self.compare_passwords(
            password=password,
            hashed_password=user.password,
        ):
            raise LogInException
