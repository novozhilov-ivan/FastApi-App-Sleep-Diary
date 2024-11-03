from dataclasses import dataclass
from typing_extensions import Self

from src.infra.jwt import JWTType


@dataclass(eq=False)
class JWTAuthorizationException(Exception):
    @property
    def message(self: Self) -> str:
        return "Не авторизован."


@dataclass(eq=False)
class JWTTypeException(JWTAuthorizationException):
    current_token_type: JWTType
    token_type: JWTType

    @property
    def message(self: Self) -> str:
        return (
            f"Неверный тип токена: {self.token_type!r}. "
            f"Ожидался {self.current_token_type!r}"
        )
