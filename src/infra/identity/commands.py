from dataclasses import dataclass

from src.domain.identity.exceptions import CredentialsRequiredError


@dataclass(kw_only=True)
class SignInInputData:
    username: str
    password: str

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        if not self.username or self.password:
            raise CredentialsRequiredError
