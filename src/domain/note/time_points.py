import operator as op

from datetime import date, time, timedelta
from typing_extensions import Self

from pydantic import (
    BaseModel,
    computed_field,
    model_validator,
)

from src.domain.exceptions import (
    NoSleepDurationException,
    TimePointsSequenceException,
)


class NoteTimePoints(BaseModel):
    bedtime_date: date
    went_to_bed: time
    fell_asleep: time
    woke_up: time
    got_up: time
    no_sleep: time = time(0, 0)

    @model_validator(mode="after")
    def validate_time_points_sequences(self: Self) -> Self:
        all_time_points_within_one_day = (
            self.went_to_bed <= self.fell_asleep <= self.woke_up <= self.got_up
        )
        got_up_after_midnight_other_time_points_within_one_day = (
            self.got_up <= self.went_to_bed <= self.fell_asleep <= self.woke_up
        )
        woke_up_and_got_up_after_midnight_other_time_points_within_one_day = (
            self.woke_up <= self.got_up <= self.went_to_bed <= self.fell_asleep
        )
        went_to_bed_within_one_day_other_time_point_after_midnight = (
            self.fell_asleep <= self.woke_up <= self.got_up <= self.went_to_bed
        )
        if any(
            (
                all_time_points_within_one_day,
                got_up_after_midnight_other_time_points_within_one_day,
                woke_up_and_got_up_after_midnight_other_time_points_within_one_day,
                went_to_bed_within_one_day_other_time_point_after_midnight,
            ),
        ):
            return self
        raise TimePointsSequenceException

    @model_validator(mode="after")
    def validate_no_sleep_duration(self: Self) -> Self:
        if self._no_sleep_duration <= self._sleep_duration:
            return self
        raise NoSleepDurationException

    @computed_field(title="Длительность сна")  # type: ignore[misc]
    @property
    def _sleep_duration(self: Self) -> timedelta:
        sleep_duration = timedelta(
            hours=op.sub(self.woke_up.hour, self.fell_asleep.hour),
            minutes=op.sub(self.woke_up.minute, self.fell_asleep.minute),
        )
        return timedelta(seconds=sleep_duration.seconds)

    @computed_field(  # type: ignore[misc]
        title="Длительность сна за вычетом времени без сна",
    )
    @property
    def _sleep_duration_minus_no_sleep(self: Self) -> timedelta:
        if self._no_sleep_duration >= self._sleep_duration:
            return timedelta(0)
        sleep_duration_minus_no_sleep = op.sub(
            self._sleep_duration,
            self._no_sleep_duration,
        )
        return timedelta(seconds=sleep_duration_minus_no_sleep.seconds)

    @computed_field(  # type: ignore[misc]
        title="Длительность времени, проведенного в постели.",
    )
    @property
    def _in_bed_duration(self: Self) -> timedelta:
        sleep_duration = timedelta(
            hours=op.sub(self.got_up.hour, self.went_to_bed.hour),
            minutes=op.sub(self.got_up.minute, self.went_to_bed.minute),
        )
        return timedelta(seconds=sleep_duration.seconds)

    @computed_field(title="Длительность отсутствия сна")  # type: ignore[misc]
    @property
    def _no_sleep_duration(self: Self) -> timedelta:
        return timedelta(
            hours=self.no_sleep.hour,
            minutes=self.no_sleep.minute,
        )
