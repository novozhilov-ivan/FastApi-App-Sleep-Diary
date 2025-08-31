from dataclasses import dataclass

from src.domain.identity.exceptions import IdentityError


@dataclass(eq=False)
class AuthenticationError(IdentityError):
    @property
    def message(self) -> str:
        return "Произошла ошибка авторизации."


@dataclass(eq=False)
class NotAuthenticatedError(AuthenticationError):
    @property
    def message(self) -> str:
        return "Необходима аутентификация."
