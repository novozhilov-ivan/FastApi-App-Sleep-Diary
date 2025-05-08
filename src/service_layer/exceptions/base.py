from dataclasses import dataclass
from typing import Self


@dataclass(eq=False)
class AuthenticationException(Exception):
    @property
    def message(self: Self) -> str:
        return "Произошла ошибка авторизации."


@dataclass(eq=False)
class NotAuthenticatedException(AuthenticationException):
    @property
    def message(self: Self) -> str:
        return "Необходима аутентификация."
