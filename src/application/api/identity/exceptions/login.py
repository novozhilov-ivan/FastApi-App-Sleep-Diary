from dataclasses import dataclass

from src.application.api.identity.exceptions.base import AuthenticationException


@dataclass(eq=False)
class LogInException(AuthenticationException):
    @property
    def message(self) -> str:
        return "Неверное имя пользователя или пароль."
