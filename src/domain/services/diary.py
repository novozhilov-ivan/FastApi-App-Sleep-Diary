from dataclasses import dataclass, field
from typing import TYPE_CHECKING
from typing_extensions import Self


if TYPE_CHECKING:
    from src.domain.entities.note import NoteEntity


@dataclass
class Diary:
    _notes: set["NoteEntity"] = field(default_factory=set, init=False)

    @classmethod
    def create(cls: type["Diary"], notes: set["NoteEntity"]) -> "Diary":
        diary = cls()
        diary._notes = set(notes)
        return diary

    def write(self: Self, note: "NoteEntity") -> None:
        if self.can_write(note):
            self._notes.add(note)

    def can_write(self: Self, note: "NoteEntity") -> bool:
        return note not in self._notes

    @property
    def notes_list(self: Self) -> set["NoteEntity"]:
        return self._notes
