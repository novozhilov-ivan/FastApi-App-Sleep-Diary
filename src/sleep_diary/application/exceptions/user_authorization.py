from dataclasses import dataclass
from typing import Self

from src.sleep_diary.application.entities import TokenType


@dataclass(eq=False)
class UserTokenAuthorizationException(Exception):
    @property
    def message(self: Self) -> str:
        return "Не авторизован."


@dataclass(eq=False)
class TokenTypeException(UserTokenAuthorizationException):
    current_token_type: TokenType
    token_type: TokenType

    @property
    def message(self: Self) -> str:
        return (
            f"Неверный тип токена: {self.token_type!r}. "
            f"Ожидался {self.current_token_type!r}"
        )
