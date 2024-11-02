from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing_extensions import Self


if TYPE_CHECKING:
    from src.infra.authorization.jwt import TokenType


@dataclass(eq=False)
class JWTAuthorizationException(Exception):
    @property
    def message(self: Self) -> str:
        return "Не авторизован."


@dataclass(eq=False)
class JWTTypeException(JWTAuthorizationException):
    current_token_type: "TokenType"
    token_type: "TokenType"

    @property
    def message(self: Self) -> str:
        return (
            f"Неверный тип токена: {self.token_type!r}. "
            f"Ожидался {self.current_token_type!r}"
        )


@dataclass(eq=False)
class JWTExpireAtFieldException(Exception):
    @property
    def message(self: Self) -> str:
        return "Одно из полей: 'expire_timedelta' или 'exp' - обязательно."
