from dataclasses import dataclass, field
from datetime import date
from uuid import UUID

from src.domain.sleep_diary.entities.note import NoteEntity
from src.domain.sleep_diary.repositories.base import INotesRepository


@dataclass
class MemoryNotesRepository(INotesRepository):
    _saved_notes: set[NoteEntity] = field(default_factory=set)

    def add(self, note: NoteEntity) -> None:
        self._saved_notes.add(note)

    def get_by_oid(self, oid: UUID) -> NoteEntity | None:
        try:
            return next(note for note in self._saved_notes if note.oid == oid)
        except StopIteration:
            return None

    def get_by_bedtime_date(
        self,
        bedtime_date: date,
        owner_oid: UUID,
    ) -> NoteEntity | None:
        try:
            return next(
                note
                for note in self._saved_notes
                if note.points.bedtime_date == bedtime_date
                and note.owner_oid == owner_oid
            )
        except StopIteration:
            return None

    def get_all_notes(self, owner_oid: UUID) -> set[NoteEntity]:
        return {note for note in self._saved_notes if note.owner_oid == owner_oid}
