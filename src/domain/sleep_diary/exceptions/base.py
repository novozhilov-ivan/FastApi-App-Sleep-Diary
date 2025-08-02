from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationException(Exception):
    @property
    def message(self) -> str:
        return "Произошла ошибка приложения."
