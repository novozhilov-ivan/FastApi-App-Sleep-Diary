from dataclasses import dataclass
from typing import cast, ClassVar, Self

from bcrypt import checkpw, gensalt, hashpw

from src.domain.entities import UserEntity
from src.domain.services import IUsersRepository
from src.domain.specifications import UserCredentialsSpecification
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
        if isinstance(self._user, NotAuthenticated):
            raise NotAuthenticatedException

        self._user = NotAuthenticated()
        cast(NotAuthenticated, self._user)

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
    def hash_password(pwd: str, encoding: str = DEFAULT_ENCODING) -> str:
        return hashpw(
            password=pwd.encode(encoding),
            salt=gensalt(),
        ).decode(encoding)

    @staticmethod
    def compare_passwords(
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
        if not self.compare_passwords(
            password=password,
            hashed_password=user.password,
        ):
            raise LogInException
