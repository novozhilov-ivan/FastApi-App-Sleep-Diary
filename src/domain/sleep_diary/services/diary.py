from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.sleep_diary.entities.note import NoteEntity


@dataclass
class DiaryService:
    _notes: set["NoteEntity"] = field(default_factory=set, init=False)

    @classmethod
    def create(
        cls: type["DiaryService"],
        notes: set["NoteEntity"],
    ) -> "DiaryService":
        diary = cls()
        diary._notes = set(notes)
        return diary

    def write(self, note: "NoteEntity") -> None:
        if self.can_write(note):
            self._notes.add(note)

    def can_write(self, note: "NoteEntity") -> bool:
        return note not in self._notes

    @property
    def notes_list(self) -> set["NoteEntity"]:
        return self._notes
