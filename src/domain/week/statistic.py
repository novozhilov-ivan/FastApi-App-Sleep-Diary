import datetime as dt
import statistics as st

from typing import Generator
from typing_extensions import Self

from pydantic import computed_field

from src.domain import note as nt, week as wk


class WeekStatistic(
    wk.WeeklyAverageDurations,
    wk.BaseWeekStatistic,
):
    @computed_field(title="Количество записей сна за неделю")  # type: ignore[misc]
    @property
    def weekly_notes_count(self: Self) -> wk.week_duration_limits:
        return self._duration_of_week

    @computed_field(title="Средняя время сна за неделю")  # type: ignore[misc]
    @property
    def average_weekly_time_in_sleep(self: Self) -> dt.time:
        return nt.timedelta_seconds_to_time(
            timedelta=self._average_weekly_sleep_duration,
        )

    @computed_field(title="Среднее время в кровати за неделю")  # type: ignore[misc]
    @property
    def average_weekly_time_in_bed(self: Self) -> dt.time:
        return nt.timedelta_seconds_to_time(
            timedelta=self._average_weekly_in_bed_duration,
        )

    @computed_field(title="Среднее время без сна за неделю")  # type: ignore[misc]
    @property
    def average_weekly_no_sleep_time(self: Self) -> dt.time:
        return nt.timedelta_seconds_to_time(
            timedelta=self._average_weekly_no_sleep_duration,
        )

    @computed_field(  # type: ignore[misc]
        title="Средняя время сна за неделю за вычетом времени без сна",
    )
    @property
    def average_weekly_time_in_sleep_minus_no_sleep(self: Self) -> dt.time:
        return nt.timedelta_seconds_to_time(
            timedelta=self._average_weekly_sleep_duration_minus_no_sleep,
        )

    @computed_field(  # type: ignore[misc]
        title="Средняя эффективность сна (%) за неделю",
    )
    @property
    def average_weekly_sleep_efficiency(self: Self) -> float:
        weekly_notes_efficiencies: Generator[float, None, None] = (
            note.sleep_efficiency
            for note in self
            if isinstance(note, nt.BaseNoteStatistic)
        )
        return round(
            number=st.mean(weekly_notes_efficiencies),
            ndigits=2,
        )
