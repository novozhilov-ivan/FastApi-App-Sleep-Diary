from dataclasses import dataclass

from src.domain.sleep_diary.exceptions.base import ApplicationException


@dataclass(eq=False)
class NoteException(ApplicationException):
    @property
    def message(self) -> str:
        return "При создании записи произошла ошибка."


@dataclass(eq=False)
class TimePointsSequenceException(NoteException):
    @property
    def message(self) -> str:
        return "Некорректная последовательность временных точек записи."


@dataclass(eq=False)
class NoSleepDurationException(NoteException):
    @property
    def message(self) -> str:
        return "Время без сна должно быть меньше или равно времени сна."
