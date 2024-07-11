import abc
import datetime as dt

from typing import Annotated, Generator
from typing_extensions import Self

from pydantic import (
    computed_field,
    conint,
)


int_duration_of_week = Annotated[int, conint(ge=1, le=7)]


class BaseWeek(set, abc.ABC):
    ...  # fmt: skip


class BaseWeeklyAverageDurations(BaseWeek, abc.ABC):
    @abc.abstractmethod
    def __compute_average_duration(
        self: Self,
        duration_name: str,
    ) -> Generator[dt.timedelta, None, None]: ...

    @computed_field(title="Средняя длительность сна за неделю")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def _duration_of_week(self: Self) -> int_duration_of_week: ...

    @computed_field(title="Средняя длительность сна за неделю")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def _average_weekly_sleep_duration(self: Self) -> dt.timedelta: ...

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность сна за неделю за вычетом времени без сна",
    )
    @property
    @abc.abstractmethod
    def _average_weekly_sleep_duration_minus_no_sleep(
        self: Self,
    ) -> dt.timedelta: ...

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность времени, проведенного в постели, за неделю.",
    )
    @property
    @abc.abstractmethod
    def _average_weekly_in_bed_duration(self: Self) -> dt.timedelta: ...

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность отсутствия сна за неделю",
    )
    @property
    @abc.abstractmethod
    def _average_weekly_no_sleep_duration(self: Self) -> dt.timedelta: ...


class BaseWeekStatistic(BaseWeeklyAverageDurations, abc.ABC):
    @computed_field(title="Количество записей сна за неделю")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def weekly_notes_count(self: Self) -> int_duration_of_week: ...

    @computed_field(title="Средняя время сна за неделю")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def average_weekly_time_in_sleep(self: Self) -> dt.time: ...

    @computed_field(title="Среднее время в кровати за неделю")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def average_weekly_time_in_bed(self: Self) -> dt.time: ...

    @computed_field(title="Среднее время без сна за неделю")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def average_weekly_no_sleep_time(self: Self) -> dt.time: ...

    @computed_field(  # type: ignore[misc]
        title="Средняя время сна за неделю за вычетом времени без сна",
    )
    @property
    @abc.abstractmethod
    def average_weekly_time_in_sleep_minus_no_sleep(self: Self) -> dt.time: ...

    @computed_field(  # type: ignore[misc]
        title="Средняя эффективность сна (%) за неделю",
    )
    @property
    @abc.abstractmethod
    def average_weekly_sleep_efficiency(self: Self) -> float: ...


class BaseWeekValueObject(
    BaseWeekStatistic,
    BaseWeek,
    abc.ABC,
):
    ...  # fmt: skip
