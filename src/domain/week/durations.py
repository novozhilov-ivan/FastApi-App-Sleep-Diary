import datetime as dt
import operator as op
import statistics as st

from typing import Generator
from typing_extensions import Self

from pydantic import computed_field

from src.domain import note as nt, week


class WeeklyAverageDurations(week.BaseWeeklyAverageDurations):
    def __compute_average_duration_of_field(
        self: Self,
        field_name: str,
    ) -> Generator[dt.timedelta, None, None]:
        timedeltas_of_week: Generator[dt.timedelta, None, None] = (
            op.attrgetter(field_name)(note)
            for note in self
            if isinstance(note, nt.NoteValueObject)
        )
        timedeltas_seconds_of_week: Generator[int, None, None] = (
            timedelta.seconds
            for timedelta in timedeltas_of_week
            if isinstance(timedelta, dt.timedelta)
        )
        yield dt.timedelta(seconds=st.mean(data=timedeltas_seconds_of_week))

    @computed_field(title="Средняя длительность сна за неделю")  # type: ignore[misc]
    @property
    def _week_duration(self: Self) -> week.int_weekly_notes_count:
        return len(self)

    @computed_field(title="Средняя длительность сна за неделю")  # type: ignore[misc]
    @property
    def _average_weekly_sleep_duration(self: Self) -> dt.timedelta:
        return next(self.__compute_average_duration_of_field("_sleep_duration"))

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность времени, проведенного в постели, за неделю.",
    )
    @property
    def _average_weekly_in_bed_duration(self: Self) -> dt.timedelta:
        return next(self.__compute_average_duration_of_field("_in_bed_duration"))

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность отсутствия сна за неделю",
    )
    @property
    def _average_weekly_no_sleep_duration(self: Self) -> dt.timedelta:
        return next(self.__compute_average_duration_of_field("_no_sleep_duration"))

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность сна за неделю за вычетом времени без сна",
    )
    @property
    def _average_weekly_sleep_duration_minus_no_sleep(
        self: Self,
    ) -> dt.timedelta:
        sleep_duration_minus_no_sleep = (
            self._average_weekly_sleep_duration.seconds
            - self._average_weekly_no_sleep_duration.seconds
        )
        return dt.timedelta(seconds=sleep_duration_minus_no_sleep)
