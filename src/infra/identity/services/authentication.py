from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import ClassVar

from bcrypt import checkpw, gensalt, hashpw

from src.domain.sleep_diary.entities.user import UserEntity
from src.domain.sleep_diary.services.base import IUsersRepository
from src.domain.sleep_diary.specifications.user_credentials import (
    UserCredentialsSpecification,
)
from src.infra.identity.exceptions.credentials import (
    UserCredentialsFormatError,
)
from src.infra.identity.exceptions.login import LogInError
from src.infra.identity.exceptions.register import (
    UserNameAlreadyExistError,
)


@dataclass
class IUserAuthenticationService(ABC):
    @abstractmethod
    def login(self, username: str, password: str) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    def register(self, username: str, password: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def unregister(self, username: str) -> None:
        raise NotImplementedError


@dataclass
class UserAuthenticationService(IUserAuthenticationService):
    _DEFAULT_ENCODING: ClassVar[str] = "utf-8"

    repository: IUsersRepository

    def login(self, username: str, password: str) -> UserEntity:
        if (user := self.repository.get_by_username(username)) is None:
            raise LogInError

        self._validate_user_password(user, password)

        return user

    def register(self, username: str, password: str) -> None:
        if self.repository.get_by_username(username) is not None:
            raise UserNameAlreadyExistError

        if not (specification := UserCredentialsSpecification(username, password)):
            raise UserCredentialsFormatError(specification)

        self.repository.add_user(
            UserEntity(
                username=username,
                password=self.hash_password(password),
            ),
        )

    def unregister(self, username: str) -> None:
        self.repository.delete_user(username)

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

    def _validate_user_password(self, user: UserEntity, password: str) -> None:
        if not self.compare_passwords(
            password=password,
            hashed_password=user.password,
        ):
            raise LogInError
