from typing import ClassVar
from typing_extensions import Self

from pydantic import ConfigDict

from src.domain.note.time_points import NoteTimePoints


class NoteValueObject(NoteTimePoints):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, NoteTimePoints):
            return NotImplemented
        return self.bedtime_date == other.bedtime_date

    def __hash__(self: Self) -> int:
        return hash(self.bedtime_date)

    def __gt__(self: Self, other: object) -> bool:
        if not isinstance(other, NoteTimePoints):
            return NotImplemented
        return self.bedtime_date > other.bedtime_date
