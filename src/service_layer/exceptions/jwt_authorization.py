from dataclasses import dataclass
from typing_extensions import Self


@dataclass(eq=False)
class JWTAuthorizationException(Exception):
    @property
    def message(self: Self) -> str:
        return "Не авторизован."
