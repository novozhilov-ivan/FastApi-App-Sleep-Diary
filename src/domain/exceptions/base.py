from dataclasses import dataclass
from typing import Self


@dataclass(eq=False)
class ApplicationException(Exception):
    @property
    def message(self: Self) -> str:
        return "Произошла ошибка приложения."
