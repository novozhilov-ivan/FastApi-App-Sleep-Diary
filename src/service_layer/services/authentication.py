from dataclasses import dataclass
from typing import ClassVar, cast
from typing_extensions import Self

from bcrypt import checkpw, gensalt, hashpw

from src.domain.entities import UserEntity
from src.domain.specifications import UserCredentialsSpecification
from src.infra.repository import IUsersRepository
from src.service_layer.exceptions import (
    LogInException,
    NotAuthenticatedException,
    UserCredentialsFormatException,
    UserNameAlreadyExistException,
)
from src.service_layer.services.base import (
    IUserAuthenticationService,
    NotAuthenticated,
)


@dataclass
class UserAuthenticationService(IUserAuthenticationService):
    DEFAULT_ENCODING: ClassVar[str] = "utf-8"

    repository: IUsersRepository

    def login(self: Self, username: str, password: str) -> None:
        user = self._validate_user(username)
        self._validate_user_password(user, password)
        self._user = user
        cast(UserEntity, self._user)

    def logout(self: Self) -> None:
        if not isinstance(self._user, NotAuthenticated):
            raise NotAuthenticatedException

        self._user = NotAuthenticated()
        cast(NotAuthenticated, self._user)

    def register(self: Self, username: str, password: str) -> None:
        if self.repository.get_by_username(username):
            raise UserNameAlreadyExistException

        if specification := UserCredentialsSpecification(username, password):
            raise UserCredentialsFormatException(specification)

        self.repository.add_user(username, self._hash_password(password))

    def unregister(self: Self, username: str) -> None:
        if not isinstance(self._user, NotAuthenticated):
            raise NotAuthenticatedException

        self.repository.delete_user(username)
        self.logout()

    @staticmethod
    def _hash_password(pwd_bytes: str, encoding: str = DEFAULT_ENCODING) -> str:
        return hashpw(
            password=pwd_bytes.encode(encoding),
            salt=gensalt(),
        ).decode(encoding)

    @staticmethod
    def _compare_passwords(
        password: str,
        hashed_password: str,
        encoding: str = DEFAULT_ENCODING,
    ) -> bool:
        return checkpw(
            password=password.encode(encoding),
            hashed_password=hashed_password.encode(encoding),
        )

    def _get_user(self: Self, username: str) -> UserEntity | None:
        return self.repository.get_by_username(username)

    def _validate_user(self: Self, username: str) -> UserEntity:
        if (user := self._get_user(username)) is None:
            raise LogInException

        return user

    def _validate_user_password(self: Self, user: UserEntity, password: str) -> None:
        if not self._compare_passwords(
            password=password,
            hashed_password=user.password,
        ):
            raise LogInException
