from datetime import time, timedelta
from typing_extensions import Self

from pydantic import computed_field

from src.domain import note


class NoteStatistic(
    note.NoteStatisticBase,
    note.NoteDurations,
    note.NoteDurationsBase,
    note.NoteValueObjectBase,
):
    @computed_field  # type: ignore[misc]
    @property
    def time_in_sleep(self: Self) -> time:
        return note.timedelta_seconds_to_time(td=self._sleep_duration_minus_no_sleep)

    @computed_field  # type: ignore[misc]
    @property
    def time_in_bed(self: Self) -> time:
        return note.timedelta_seconds_to_time(td=self._in_bed_duration)

    @computed_field  # type: ignore[misc]
    @property
    def sleep_efficiency(self: Self) -> float:
        if self._in_bed_duration == timedelta(0):
            return round(0, 2)
        efficiency = self._sleep_duration_minus_no_sleep / self._in_bed_duration
        return round(efficiency, 2)
