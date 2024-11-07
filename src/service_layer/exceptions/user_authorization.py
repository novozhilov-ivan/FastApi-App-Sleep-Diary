from dataclasses import dataclass
from typing_extensions import Self

from src.service_layer.entities import TokenType


@dataclass(eq=False)
class UserAuthorizationException(Exception):
    @property
    def message(self: Self) -> str:
        return "Не авторизован."


@dataclass(eq=False)
class TokenTypeException(UserAuthorizationException):
    current_token_type: TokenType
    token_type: TokenType

    @property
    def message(self: Self) -> str:
        return (
            f"Неверный тип токена: {self.token_type!r}. "
            f"Ожидался {self.current_token_type!r}"
        )
