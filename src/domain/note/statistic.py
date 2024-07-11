import abc
import datetime as dt
import operator as op

from typing_extensions import Self

from pydantic import computed_field

from src.domain import note as nt


class NoteStatistic(
    nt.NoteDurations,
    nt.BaseNoteStatistic,
    abc.ABC,
):
    @computed_field(title="Время сна")  # type: ignore[misc]
    @property
    def time_in_sleep(self: Self) -> dt.time:
        return nt.timedelta_seconds_to_time(self._sleep_duration)

    @computed_field(title="Время в кровати")  # type: ignore[misc]
    @property
    def time_in_bed(self: Self) -> dt.time:
        return nt.timedelta_seconds_to_time(self._in_bed_duration)

    @computed_field(title="Время сна")  # type: ignore[misc]
    @property
    def time_in_sleep_minus_no_sleep(self: Self) -> dt.time:
        return nt.timedelta_seconds_to_time(self._sleep_duration_minus_no_sleep)

    @computed_field(title="Эффективность сна (%)")  # type: ignore[misc]
    @property
    def sleep_efficiency(self: Self) -> float:
        if self._in_bed_duration == dt.timedelta(0):
            return 0.0
        return round(
            number=op.truediv(
                self._sleep_duration_minus_no_sleep,
                self._in_bed_duration,
            ),
            ndigits=2,
        )
