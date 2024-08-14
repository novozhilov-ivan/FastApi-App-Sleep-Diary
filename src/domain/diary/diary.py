from typing_extensions import Self

from pydantic import BaseModel, PrivateAttr

from src.domain.note import NoteValueObject


class Diary(BaseModel):
    _notes: set[NoteValueObject] = PrivateAttr(default_factory=set)

    def write(self: Self, note: NoteValueObject) -> None:
        if self.can_write(note):
            self._notes.add(note)

    def can_write(self: Self, note: NoteValueObject) -> bool:
        return note not in self._notes

    @property
    def notes_list(self: Self) -> set[NoteValueObject]:
        return self._notes
