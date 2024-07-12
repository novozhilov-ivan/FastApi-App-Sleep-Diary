from typing import ClassVar
from typing_extensions import Self

from pydantic import ConfigDict

from src.domain.note import base, statistic, validators


class NoteValueObject(
    statistic.NoteStatistic,
    validators.NoSleepDurationValidator,
    validators.TimePointsSequencesValidator,
    base.BaseNoteValueObject,
):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, base.BaseNoteDateTimePoints):
            return NotImplemented
        return self.bedtime_date == other.bedtime_date

    def __hash__(self: Self) -> int:
        return hash(self.bedtime_date)
