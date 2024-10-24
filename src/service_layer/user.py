from dataclasses import InitVar, dataclass, field
from typing_extensions import Self

from bcrypt import checkpw, gensalt, hashpw

from src.domain.entities.user import UserEntity
from src.infrastructure.repository.base import BaseUserRepository


response_invalid_username_or_password_401 = "invalid username or password"


@dataclass
class UserAuthenticationService:
    user_repository: InitVar[BaseUserRepository]
    received_username: InitVar[str]
    received_password: InitVar[bytes]

    user: UserEntity = field(init=False)

    def __post_init__(
        self: Self,
        user_repository: BaseUserRepository,
        received_username: str,
        received_password: bytes,
    ) -> None:
        user: UserEntity | None = self.get_user(received_username, user_repository)
        self.validate_credentials(user, received_password)

    def validate_credentials(
        self: Self,
        user: UserEntity | None,
        received_password: bytes,
    ) -> None:
        self.validate_user()
        self.user: UserEntity
        self.validate_user_password(user, received_password)

    @staticmethod
    def hash_password(pwd_bytes: bytes, decode_from: str = "utf-8") -> str:
        return hashpw(pwd_bytes, gensalt()).decode(decode_from)

    @staticmethod
    def validate_password(password: bytes, hashed_password: bytes) -> bool:
        return checkpw(password=password, hashed_password=hashed_password)

    @staticmethod
    def get_user(
        received_username: str,
        user_repository: BaseUserRepository,
    ) -> UserEntity | None:
        return user_repository.get_by_username(received_username)

    def validate_user(self: Self) -> None:
        if self.user is None:
            raise AuthenticationException(response_invalid_username_or_password_401)

    def validate_user_password(
        self: Self,
        user: UserEntity,
        received_password: bytes,
    ) -> None:
        if not self.validate_password(
            password=received_password,
            hashed_password=user.password,
        ):
            raise AuthenticationException(response_invalid_username_or_password_401)
