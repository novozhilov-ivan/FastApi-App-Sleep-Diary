from dataclasses import dataclass

from src.identity.domain.exceptions import CredentialsRequiredError


@dataclass(kw_only=True)
class SignInInputData:
    username: str
    password: str

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.username:
            raise CredentialsRequiredError
