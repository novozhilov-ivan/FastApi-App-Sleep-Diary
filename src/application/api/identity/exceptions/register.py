from dataclasses import dataclass

from src.application.api.identity.exceptions.base import AuthenticationException


@dataclass(eq=False)
class UserRegisterException(AuthenticationException):
    @property
    def message(self) -> str:
        return "Произошла ошибка при регистрации пользователя."


@dataclass(eq=False)
class UserNameAlreadyExistException(UserRegisterException):
    @property
    def message(self) -> str:
        return "Это имя пользователя занято."
