from dataclasses import dataclass, field
from datetime import date
from typing_extensions import Self
from uuid import UUID

from src.domain.entities import NoteEntity
from src.domain.services import INotesRepository


@dataclass
class MemoryNotesRepository(INotesRepository):
    _saved_notes: set[NoteEntity] = field(default_factory=set)

    def add(self: Self, note: NoteEntity) -> None:
        self._saved_notes.add(note)

    def get_by_oid(self: Self, oid: UUID) -> NoteEntity | None:
        try:
            return next(note for note in self._saved_notes if note.oid == oid)
        except StopIteration:
            return None

    def get_by_bedtime_date(
        self: Self,
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

    def get_all_notes(self: Self, owner_oid: UUID) -> set[NoteEntity]:
        return {note for note in self._saved_notes if note.owner_oid == owner_oid}
