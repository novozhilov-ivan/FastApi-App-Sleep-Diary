import abc

from datetime import time, timedelta
from typing import Annotated, Callable, Type, TypeAlias

from typing_extensions import Self

from pydantic import (
    BaseModel,
    Field,
    computed_field,
    conint,
)

from src.domain import note as nt


int_weekly_notes_count = Annotated[int, conint(ge=1, le=7)]


class WeekBase(BaseModel, abc.ABC):
    notes: set[nt.NoteBase] = Field(
        title="Неделя с записями сна",
        min_length=1,
        max_length=7,
    )


class WeekDurationsBase(WeekBase, abc.ABC):
    @computed_field(  # type: ignore[misc]
        title="Средняя длительность сна за неделю",
    )
    @property
    @abc.abstractmethod
    def _average_weekly_sleep_duration(self: Self) -> timedelta: ...

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность сна за неделю за вычетом времени без сна",
    )
    @property
    @abc.abstractmethod
    def _average_weekly_sleep_duration_minus_no_sleep(self: Self) -> timedelta: ...

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность времени, проведенного в постели, за неделю.",
    )
    @property
    @abc.abstractmethod
    def _average_weekly_in_bed_duration(self: Self) -> timedelta: ...

    @computed_field(  # type: ignore[misc]
        title="Средняя длительность отсутствия сна за неделю",
    )
    @property
    @abc.abstractmethod
    def _average_weekly_no_sleep_duration(self: Self) -> timedelta: ...


class WeekStatisticBase(WeekDurationsBase, abc.ABC):
    @computed_field(  # type: ignore[misc]
        title="Количество записей сна за неделю",
    )
    @property
    @abc.abstractmethod
    def weekly_notes_count(self: Self) -> int_weekly_notes_count: ...

    @computed_field(  # type: ignore[misc]
        title="Средняя время сна за неделю",
    )
    @property
    @abc.abstractmethod
    def average_weekly_time_in_sleep(self: Self) -> time: ...

    @computed_field(  # type: ignore[misc]
        title="Среднее время в кровати за неделю",
    )
    @property
    @abc.abstractmethod
    def average_weekly_time_in_bed(self: Self) -> time: ...

    @computed_field(  # type: ignore[misc]
        title="Среднее время без сна за неделю",
    )
    @property
    @abc.abstractmethod
    def average_weekly_no_sleep_time(self: Self) -> time: ...

    @computed_field(  # type: ignore[misc]
        title="Средняя эффективность сна (%) за неделю",
    )
    @property
    @abc.abstractmethod
    def average_weekly_sleep_efficiency(self: Self) -> float: ...