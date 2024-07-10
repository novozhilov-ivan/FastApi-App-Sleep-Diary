from typing import ClassVar

from pydantic import ConfigDict

from src.domain import note


class NoteEntity(
    note.NoteValueObject,
    note.BaseNoteEntity,
):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=False,
        extra="forbid",
    )
