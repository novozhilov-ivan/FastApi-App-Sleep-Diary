from datetime import datetime
from typing import ClassVar
from typing_extensions import Self
from uuid import UUID

from pydantic import ConfigDict

from src.domain.note.time_points import NoteTimePoints


class NoteEntity(NoteTimePoints):
    oid: UUID
    created_at: datetime
    updated_at: datetime

    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra="forbid",
    )

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, NoteEntity):
            return NotImplemented
        return self.oid == other.oid
