import uuid

from datetime import datetime
from typing import ClassVar
from typing_extensions import Self

from pydantic import ConfigDict

from src.domain.note.statistic import NoteStatistic
from src.domain.note.value_object import NoteValueObject


class NoteEntity(NoteValueObject, NoteStatistic):
    oid: uuid.UUID
    created_at: datetime
    updated_at: datetime

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=False,
        extra="forbid",
    )

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, NoteEntity):
            return NotImplemented
        return (
            self.oid == other.oid
            and self.bedtime_date == other.bedtime_date
            and self.created_at == other.created_at
            and self.updated_at == other.updated_at
        )
