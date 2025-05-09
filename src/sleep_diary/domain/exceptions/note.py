from dataclasses import dataclass
from typing import Self

from src.sleep_diary.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class NoteException(ApplicationException):
    @property
    def message(self: Self) -> str:
        return "При создании записи произошла ошибка."


@dataclass(eq=False)
class TimePointsSequenceException(NoteException):
    @property
    def message(self: Self) -> str:
        return "Некорректная последовательность временных точек записи."


@dataclass(eq=False)
class NoSleepDurationException(NoteException):
    @property
    def message(self: Self) -> str:
        return "Время без сна должно быть меньше или равно времени сна."
