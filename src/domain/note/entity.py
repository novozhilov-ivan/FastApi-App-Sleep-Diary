import datetime as dt

from typing import ClassVar

from pydantic import ConfigDict, Field

from src.domain.note.statistic import NoteStatistic


class NoteEntity(NoteStatistic):
    oid: int = Field(gt=0)
    created_at: dt.datetime
    updated_at: dt.datetime
    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=False,
        extra="forbid",
    )
