from typing_extensions import Self


class ErrorNoteBase(Exception):
    @property
    def message(self: Self) -> str:
        return "При создании записи произошла ошибка."


class ErrorTimePointsSequence(ErrorNoteBase):
    @property
    def message(self: Self) -> str:
        return "Некорректная последовательность временных точек записи."


class ErrorNoSleepDuration(ErrorNoteBase):
    @property
    def message(self: Self) -> str:
        return "Время без сна должно быть меньше или равно времени сна."
