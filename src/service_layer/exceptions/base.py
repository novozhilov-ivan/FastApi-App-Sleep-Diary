from dataclasses import dataclass
from typing_extensions import Self


@dataclass(eq=False)
class AuthorizationException(Exception):
    @property
    def message(self: Self) -> str:
        return "Произошла ошибка авторизации."
