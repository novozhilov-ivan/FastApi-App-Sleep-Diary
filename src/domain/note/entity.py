from typing import ClassVar

from pydantic import ConfigDict

from src.domain.note import base, value_object


class NoteEntity(
    value_object.NoteValueObject,
    base.BaseNoteEntity,
):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=False,
        extra="forbid",
    )
