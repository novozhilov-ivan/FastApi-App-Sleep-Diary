from dataclasses import dataclass
from datetime import date

from src.domain.sleep_diary.exceptions.base import ApplicationException


@dataclass(eq=False)
class NonUniqueNoteBedtimeDateException(ApplicationException):
    bedtime_date: date

    @property
    def message(self) -> str:
        return f"Запись о сне с датой {self.bedtime_date} уже существует в дневнике."
