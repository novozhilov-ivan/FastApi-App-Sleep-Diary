from typing_extensions import Self


class NoteBaseError(Exception):
    @property
    def message(self: Self) -> str:
        return "При создании записи произошла ошибка."


class TimePointsSequenceError(NoteBaseError):
    @property
    def message(self: Self) -> str:
        return "Некорректная последовательность временных точек записи."


class NoSleepDurationError(NoteBaseError):
    @property
    def message(self: Self) -> str:
        return "Время без сна должно быть меньше или равно времени сна."
