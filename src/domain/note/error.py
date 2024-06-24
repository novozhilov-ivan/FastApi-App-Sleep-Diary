from src.domain.error.error import NoteBaseError


class SleepTimePointError(NoteBaseError):
    @property
    def message(self) -> str:
        return "При проверки поля с временем произошла ошибка."


class NoSleepTimeError(NoteBaseError):
    @property
    def message(self) -> str:
        return "Время без сна должно быть меньше или равно времени сна."
