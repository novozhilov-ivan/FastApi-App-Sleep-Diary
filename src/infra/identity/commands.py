from dataclasses import dataclass

from src.domain.identity.exceptions import (
    CredentialsRequiredError,
    PasswordsMismatchError,
)


@dataclass(kw_only=True)
class SignInInputData:
    username: str
    password: str

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.username or not self.password:
            raise CredentialsRequiredError


@dataclass(kw_only=True)
class SignUpInputData:
    username: str
    plain_password_first: str
    plain_password_second: str

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if (
            not self.username
            or not self.plain_password_first
            or not self.plain_password_second
        ):
            raise CredentialsRequiredError
        if self.plain_password_first != self.plain_password_second:
            raise PasswordsMismatchError

    def to_sign_in_command(self) -> SignInInputData:
        return SignInInputData(
            username=self.username,
            password=self.plain_password_first,
        )
