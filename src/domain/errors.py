from dataclasses import dataclass
from typing_extensions import Self


@dataclass
class ErrorNoteAlreadyExist(Exception):
    message: str = "При создании записи произошла ошибка."

    @property
    def message(self: Self) -> str:
        return self.message
