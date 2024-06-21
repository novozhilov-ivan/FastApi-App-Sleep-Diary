

class NoteBaseError(Exception):
    @property
    def message(self) -> str:
        return "При создании записи произошла ошибка."