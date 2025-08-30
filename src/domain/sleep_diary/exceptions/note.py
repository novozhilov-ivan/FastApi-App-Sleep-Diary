from dataclasses import dataclass

from src.domain.sleep_diary.exceptions.base import ApplicationError


@dataclass(eq=False)
class NoteError(ApplicationError):
    @property
    def message(self) -> str:
        return "При создании записи произошла ошибка."


@dataclass(eq=False)
class TimePointsSequenceError(NoteError):
    @property
    def message(self) -> str:
        return "Некорректная последовательность временных точек записи."


@dataclass(eq=False)
class NoSleepDurationError(NoteError):
    @property
    def message(self) -> str:
        return "Время без сна должно быть меньше или равно времени сна."
