from datetime import timedelta

from pydantic import model_validator
from typing_extensions import Self

from src.domain.note.base import NoteBase
from src.domain.note.error import NoSleepDurationError, TimePointsSequenceError


class NoteFieldsValidators(NoteBase):
    @model_validator(mode="after")
    def validate_time_points_sequences(self) -> Self:
        if (
            self.went_to_bed <= self.fell_asleep <= self.woke_up <= self.got_up
            or self.got_up <= self.went_to_bed <= self.fell_asleep <= self.woke_up
            or self.woke_up <= self.got_up <= self.went_to_bed <= self.fell_asleep
            or self.fell_asleep <= self.woke_up <= self.got_up <= self.went_to_bed
        ):
            return self
        raise TimePointsSequenceError

    @model_validator(mode="after")
    def validate_no_sleep_time_duration(self) -> Self:
        if self.fell_asleep <= self.woke_up:
            sleep_timedelta = timedelta(
                hours=self.woke_up.hour - self.fell_asleep.hour,
                minutes=self.woke_up.minute - self.fell_asleep.minute,
            )
        else:
            one_day_timedelta = timedelta(days=1)
            inverse_sleep_timedelta = timedelta(
                hours=self.fell_asleep.hour + self.woke_up.hour,
                minutes=self.fell_asleep.minute + self.woke_up.minute,
            )
            sleep_timedelta = one_day_timedelta - inverse_sleep_timedelta

        no_sleep_timedelta = timedelta(
            hours=self.no_sleep.hour,
            minutes=self.no_sleep.minute,
        )
        if no_sleep_timedelta < sleep_timedelta:
            return self
        raise NoSleepDurationError
