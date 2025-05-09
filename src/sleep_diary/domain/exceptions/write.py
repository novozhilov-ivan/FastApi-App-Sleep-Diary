from dataclasses import dataclass
from datetime import date
from typing import Self

from src.sleep_diary.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class NonUniqueNoteBedtimeDateException(ApplicationException):
    bedtime_date: date

    @property
    def message(self: Self) -> str:
        return f"Запись о сне с датой {self.bedtime_date} уже существует в дневнике."
