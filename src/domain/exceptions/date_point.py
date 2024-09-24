from dataclasses import dataclass
from typing_extensions import Self

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class DatePointException(ApplicationException):
    @property
    def message(self: Self) -> str:
        return "Ошибка создания даты сна."


@dataclass(eq=False)
class DatePointTypeException(DatePointException):
    @property
    def message(self: Self) -> str:
        return "Недопустимый тип данных временной точки, используйте date или str."


@dataclass(eq=False)
class DatePointIsoFormatException(DatePointException):
    @property
    def message(self: Self) -> str:
        return "Недопустимый iso-формат даты сна."
