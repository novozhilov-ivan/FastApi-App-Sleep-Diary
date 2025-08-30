from dataclasses import dataclass


@dataclass(eq=False)
class ApplicationError(Exception):
    @property
    def message(self) -> str:
        return "Произошла ошибка приложения."
