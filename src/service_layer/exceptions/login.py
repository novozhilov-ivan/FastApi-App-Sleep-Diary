from dataclasses import dataclass
from typing import Self

from src.service_layer.exceptions.base import AuthenticationException


@dataclass(eq=False)
class LogInException(AuthenticationException):
    @property
    def message(self: Self) -> str:
        return "Неверное имя пользователя или пароль."
