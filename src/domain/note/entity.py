import uuid

from datetime import datetime
from typing import ClassVar

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
