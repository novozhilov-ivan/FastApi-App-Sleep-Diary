from dataclasses import dataclass
from typing import Self


@dataclass(eq=False)
class JWTException(Exception):
    @property
    def message(self: Self) -> str:
        return "Невалидный токен."


@dataclass(eq=False)
class DecodeJWTException(JWTException):
    pass


@dataclass(eq=False)
class EncodeJWTException(JWTException):
    pass
