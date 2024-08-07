import datetime as dt
import operator as op
import statistics as st

from typing import Annotated, Generator
from typing_extensions import Self

from pydantic import computed_field, conint

from src.domain import note as nt


week_duration_limits = Annotated[int, conint(ge=1, le=7)]


class Week(set):

    def is_writable(self: Self) -> bool:
        return len(self) < 7

    def __compute_average_duration(
        self: Self,
        duration_name: str,
    ) -> Generator[dt.timedelta, None, None]:
        all_durations_in_seconds_of_week: Generator[int, None, None] = (
            op.attrgetter(f"{duration_name}.seconds")(note)
            for note in self
            if isinstance(note, nt.NoteTimePoints)
        )
        yield dt.timedelta(seconds=st.mean(all_durations_in_seconds_of_week))

    @computed_field(title="Продолжительность недели")  # type: ignore[misc]
    @property
    def _duration_of_week(self: Self) -> week_duration_limits:
        return len(self)

    @computed_field(title="Средняя длительность сна за неделю")  # type: ignore[misc]
    @property
    def _average_weekly_sleep_duration(self: Self) -> dt.timedelta:
        return next(self.__compute_average_duration("_sleep_duration"))

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность времени, проведенного в постели, за неделю.",
    )
    @property
    def _average_weekly_in_bed_duration(self: Self) -> dt.timedelta:
        return next(self.__compute_average_duration("_in_bed_duration"))

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность отсутствия сна за неделю",
    )
    @property
    def _average_weekly_no_sleep_duration(self: Self) -> dt.timedelta:
        return next(self.__compute_average_duration("_no_sleep_duration"))

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность сна за неделю за вычетом времени без сна",
    )
    @property
    def _average_weekly_sleep_duration_minus_no_sleep(
        self: Self,
    ) -> dt.timedelta:
        return next(
            self.__compute_average_duration("_sleep_duration_minus_no_sleep"),
        )

    @computed_field(title="Количество записей сна за неделю")  # type: ignore[misc]
    @property
    def weekly_notes_count(self: Self) -> week_duration_limits:
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
            if isinstance(note, nt.NoteStatistic)
        )
        return round(
            number=st.mean(weekly_notes_efficiencies),
            ndigits=2,
        )
