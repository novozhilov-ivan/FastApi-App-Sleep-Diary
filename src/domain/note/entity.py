import datetime as dt
import uuid

from typing import ClassVar

from pydantic import ConfigDict, Field

from src.domain.note.statistic import NoteStatistic


class NoteEntity(NoteStatistic):
    oid: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
    )
    created_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(tz=dt.UTC),
    )
    updated_at: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(tz=dt.UTC),
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=False,
        extra="forbid",
    )
