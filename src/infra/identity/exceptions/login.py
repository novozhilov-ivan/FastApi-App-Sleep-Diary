from dataclasses import dataclass

from src.infra.identity.exceptions.base import AuthenticationError


@dataclass(eq=False)
class LogInError(AuthenticationError):
    @property
    def message(self) -> str:
        return "Неверное имя пользователя или пароль."
