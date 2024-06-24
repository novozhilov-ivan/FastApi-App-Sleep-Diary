from src.domain.error.error import NoteBaseError


class ValidateTimePointNoteFieldError(NoteBaseError):
    @property
    def message(self) -> str:
        return "При проверки поля с временем произошла ошибка."
