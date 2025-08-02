from dataclasses import dataclass


@dataclass(eq=False)
class AuthenticationException(Exception):
    @property
    def message(self) -> str:
        return "Произошла ошибка авторизации."


@dataclass(eq=False)
class NotAuthenticatedException(AuthenticationException):
    @property
    def message(self) -> str:
        return "Необходима аутентификация."
