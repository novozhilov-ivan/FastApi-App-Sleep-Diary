from dataclasses import dataclass
from typing import TYPE_CHECKING
from typing_extensions import Self


if TYPE_CHECKING:
    from src.infrastructure.authorization.base import JWTTypes


@dataclass(eq=False)
class JWTAuthorizationException(Exception):
    @property
    def message(self: Self) -> str:
        return "Не авторизован."


class JWTTypeException(JWTAuthorizationException):
    current_token_type: "JWTTypes"
    token_type: "JWTTypes"

    @property
    def message(self: Self) -> str:
        return (
            f"Неверный тип токена: {self.token_type!r}. "
            f"Ожидался {self.current_token_type!r}"
        )
