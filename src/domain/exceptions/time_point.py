from dataclasses import dataclass
from typing_extensions import Self

from src.domain.exceptions import ApplicationException


@dataclass(eq=False)
class TimePointException(ApplicationException):
    @property
    def message(self: Self) -> str:
        return "Ошибка создания временной точки."


@dataclass(eq=False)
class TimePointTypeException(TimePointException):
    @property
    def message(self: Self) -> str:
        return "Недопустимый тип данных временной точки, используйте time или str."


@dataclass(eq=False)
class TimePointFormatException(TimePointException):
    @property
    def message(self: Self) -> str:
        return "Недопустимый формат временной точки, используйте iso-формат."
