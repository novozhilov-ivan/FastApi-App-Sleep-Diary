from dataclasses import dataclass, field
from uuid import UUID

from src.domain.sleep_diary.entities.note import NoteEntity
from src.domain.sleep_diary.repositories.base import IWeeksRepository


@dataclass
class MemoryWeeksRepository(IWeeksRepository):
    _notes: set[NoteEntity] = field(default_factory=set)

    def get_weeks(self, owner_oid: UUID) -> list[set[NoteEntity]]:
        return []
