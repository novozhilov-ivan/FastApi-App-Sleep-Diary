from dataclasses import dataclass
from typing_extensions import Self

from src.service_layer.exceptions.base import AuthenticationException


@dataclass(eq=False)
class UserRegisterException(AuthenticationException):
    @property
    def message(self: Self) -> str:
        return "Произошла ошибка при регистрации пользователя."


@dataclass(eq=False)
class UserNameAlreadyExistException(UserRegisterException):
    @property
    def message(self: Self) -> str:
        return "Это имя пользователя занято."
