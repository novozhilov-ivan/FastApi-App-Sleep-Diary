from dataclasses import dataclass
from typing_extensions import Self

from src.service_layer.entities import TokenType
from src.service_layer.exceptions.jwt_authorization import JWTAuthorizationException


@dataclass(eq=False)
class JWTTypeException(JWTAuthorizationException):
    current_token_type: TokenType
    token_type: TokenType

    @property
    def message(self: Self) -> str:
        return (
            f"Неверный тип токена: {self.token_type!r}. "
            f"Ожидался {self.current_token_type!r}"
        )
