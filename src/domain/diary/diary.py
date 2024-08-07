from typing_extensions import Self

from pydantic import BaseModel, PrivateAttr

from src.domain import note as nt


class Diary(BaseModel):
    _notes: set[nt.NoteValueObject] = PrivateAttr(default_factory=set)

    def write(self: Self, note: nt.NoteValueObject) -> None:
        if self.can_write(note):
            self._notes.add(note)

    def can_write(self: Self, note: nt.NoteValueObject) -> bool:
        return note not in self._notes

    @property
    def notes_list(self: Self) -> set[nt.NoteValueObject]:
        return self._notes
