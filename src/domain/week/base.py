import abc

from datetime import time, timedelta
from typing import Annotated, ClassVar
from typing_extensions import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
    conint,
)

from src.domain import note


int_weekly_notes_count = Annotated[int, conint(ge=1, le=7)]


# TODO Наследоваться от set
# TODO Сделать ограничения
class BaseWeek(BaseModel, abc.ABC):
    notes: set[note.NoteValueObject] = Field(
        title="Неделя с записями сна",
        min_length=1,
        max_length=7,
    )
    model_config: ClassVar = ConfigDict(extra="forbid")


class BaseWeeklyAverageDurations(BaseWeek, abc.ABC):
    @computed_field(title="Средняя длительность сна за неделю")  # type: ignore[misc]
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


class BaseWeekStatistic(BaseWeeklyAverageDurations, abc.ABC):
    @computed_field(title="Количество записей сна за неделю")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def weekly_notes_count(self: Self) -> int_weekly_notes_count: ...

    @computed_field(title="Средняя время сна за неделю")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def average_weekly_time_in_sleep(self: Self) -> time: ...

    @computed_field(title="Среднее время в кровати за неделю")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def average_weekly_time_in_bed(self: Self) -> time: ...

    @computed_field(title="Среднее время без сна за неделю")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def average_weekly_no_sleep_time(self: Self) -> time: ...

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
