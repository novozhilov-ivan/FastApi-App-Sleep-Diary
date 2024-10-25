from dataclasses import dataclass
from typing_extensions import Self

from src.service_layer.exceptions.base import AuthenticationException


@dataclass
class LogInException(AuthenticationException):
    wrong_credentials: str

    @property
    def message(self: Self) -> str:
        return f"Ошибка авторизации. {self.wrong_credentials}"
