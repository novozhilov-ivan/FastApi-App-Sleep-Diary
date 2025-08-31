from dataclasses import dataclass

from src.infra.identity.exceptions.base import AuthenticationError


@dataclass(eq=False)
class UserRegisterError(AuthenticationError):
    @property
    def message(self) -> str:
        return "Произошла ошибка при регистрации пользователя."


@dataclass(eq=False)
class UserNameAlreadyExistError(UserRegisterError):
    @property
    def message(self) -> str:
        return "Это имя пользователя занято."
