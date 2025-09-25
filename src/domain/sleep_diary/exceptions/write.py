from dataclasses import dataclass
from datetime import date

from src.domain.sleep_diary.exceptions.base import ApplicationError


@dataclass(eq=False)
class NonUniqueNoteBedtimeDateError(ApplicationError):
    bedtime_date: date

    @property
    def message(self) -> str:
        return f"Запись о сне с датой {self.bedtime_date} уже существует в дневнике."


@dataclass(eq=False)
class NoteNotFoundError(ApplicationError):
    @property
    def message(self) -> str:
        return "Запись не найдена."
