class NoteBaseError(Exception):
    @property
    def message(self) -> str:
        return "При создании записи произошла ошибка."


class TimePointsSequenceError(NoteBaseError):
    @property
    def message(self) -> str:
        return "Некорректная последовательность временных точек записи."


class NoSleepDurationError(NoteBaseError):
    @property
    def message(self) -> str:
        return "Время без сна должно быть меньше или равно времени сна."
