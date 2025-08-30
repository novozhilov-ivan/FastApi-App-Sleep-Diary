from dataclasses import dataclass


@dataclass(eq=False)
class AuthenticationError(Exception):
    @property
    def message(self) -> str:
        return "Произошла ошибка авторизации."


@dataclass(eq=False)
class NotAuthenticatedError(AuthenticationError):
    @property
    def message(self) -> str:
        return "Необходима аутентификация."
