import datetime as dt
import operator as op

from typing_extensions import Self

from pydantic import (
    BaseModel,
    Field,
    computed_field,
    model_validator,
)

from src.domain.note.error import NoSleepDurationError, TimePointsSequenceError


class NoteTimePoints(BaseModel):
    bedtime_date: dt.date = Field(
        title="Дата отхода ко сну",
        description="",
        examples=["2020-12-12", "2021-01-20"],
    )
    went_to_bed: dt.time = Field(
        title="Время отхода ко сну",
        description="",
        examples=["01:00", "13:00"],
    )
    fell_asleep: dt.time = Field(
        title="Время засыпания",
        description="",
        examples=["03:00", "15:00"],
    )
    woke_up: dt.time = Field(
        title="Время пробуждения",
        description="",
        examples=["11:00", "23:00"],
    )
    got_up: dt.time = Field(
        title="Время подъема",
        description="",
        examples=["13:00", "01:00"],
    )
    no_sleep: dt.time = Field(
        default=dt.time(hour=0, minute=0),
        title="Время отсутствия сна",
        description="",
        examples=["00:00", "00:20"],
    )

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
        raise TimePointsSequenceError

    @model_validator(mode="after")
    def validate_no_sleep_duration(self: Self) -> Self:
        if self._no_sleep_duration <= self._sleep_duration:
            return self
        raise NoSleepDurationError

    @computed_field(title="Длительность сна")  # type: ignore[misc]
    @property
    def _sleep_duration(self: Self) -> dt.timedelta:
        sleep_duration = dt.timedelta(
            hours=op.sub(self.woke_up.hour, self.fell_asleep.hour),
            minutes=op.sub(self.woke_up.minute, self.fell_asleep.minute),
        )
        return dt.timedelta(seconds=sleep_duration.seconds)

    @computed_field(  # type: ignore[misc]
        title="Длительность сна за вычетом времени без сна",
    )
    @property
    def _sleep_duration_minus_no_sleep(self: Self) -> dt.timedelta:
        if self._no_sleep_duration >= self._sleep_duration:
            return dt.timedelta(0)
        sleep_duration_minus_no_sleep = op.sub(
            self._sleep_duration,
            self._no_sleep_duration,
        )
        return dt.timedelta(seconds=sleep_duration_minus_no_sleep.seconds)

    @computed_field(  # type: ignore[misc]
        title="Длительность времени, проведенного в постели.",
    )
    @property
    def _in_bed_duration(self: Self) -> dt.timedelta:
        sleep_duration = dt.timedelta(
            hours=op.sub(self.got_up.hour, self.went_to_bed.hour),
            minutes=op.sub(self.got_up.minute, self.went_to_bed.minute),
        )
        return dt.timedelta(seconds=sleep_duration.seconds)

    @computed_field(title="Длительность отсутствия сна")  # type: ignore[misc]
    @property
    def _no_sleep_duration(self: Self) -> dt.timedelta:
        return dt.timedelta(
            hours=self.no_sleep.hour,
            minutes=self.no_sleep.minute,
        )
