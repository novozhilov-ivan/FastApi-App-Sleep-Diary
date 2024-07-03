import abc

from typing_extensions import Self

from pydantic import model_validator

from src.domain import note


class TimePointsSequencesValidator(
    note.NoteValueObjectBase,
    abc.ABC,
):
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
        raise note.TimePointsSequenceError


class NoSleepDurationValidator(
    note.NoteDurationsBase,
    abc.ABC,
):
    @model_validator(mode="after")
    def validate_no_sleep_duration(self: Self) -> Self:
        if self._no_sleep_duration <= self._sleep_duration_without_no_sleep:
            return self
        raise note.NoSleepDurationError
