from dataclasses import dataclass
from typing import Self

from src.sleep_diary.application.exceptions.base import AuthenticationException


@dataclass(eq=False)
class LogInException(AuthenticationException):
    @property
    def message(self: Self) -> str:
        return "Неверное имя пользователя или пароль."
