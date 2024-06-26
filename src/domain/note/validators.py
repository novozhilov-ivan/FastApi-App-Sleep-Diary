from pydantic import model_validator
from typing_extensions import Self

from src.domain.note.base import NoteBase
from src.domain.note.error import NoSleepDurationError, TimePointsSequenceError
from src.domain.note.durations import NoteDurations


class NoteFieldsValidators(NoteDurations, NoteBase):
    @model_validator(mode="after")
    def validate_time_points_sequences(self: Self) -> Self:
        if (
            self.went_to_bed <= self.fell_asleep <= self.woke_up <= self.got_up
            or self.got_up <= self.went_to_bed <= self.fell_asleep <= self.woke_up
            or self.woke_up <= self.got_up <= self.went_to_bed <= self.fell_asleep
            or self.fell_asleep <= self.woke_up <= self.got_up <= self.went_to_bed
        ):
            return self
        raise TimePointsSequenceError

    @model_validator(mode="after")
    def validate_no_sleep_duration(self: Self) -> Self:
        if self._no_sleep_duration <= self._sleep_duration_without_the_no_sleep:
            return self
        raise NoSleepDurationError
