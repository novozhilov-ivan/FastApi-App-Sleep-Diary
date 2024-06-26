import abc
from datetime import date, time, timedelta

from pydantic import BaseModel, ConfigDict, Field, computed_field
from typing_extensions import Self


class NoteBase(BaseModel, abc.ABC):
    bedtime_date: date = Field(
        title="Дата отхода ко сну",
        description="",
        examples=["2020-12-12", "2021-01-20"],
    )
    went_to_bed: time = Field(
        title="Время отхода ко сну",
        description="",
        examples=["01:00", "13:00"],
    )
    fell_asleep: time = Field(
        title="Время засыпания",
        description="",
        examples=["03:00", "15:00"],
    )
    woke_up: time = Field(
        title="Время пробуждения",
        description="",
        examples=["11:00", "23:00"],
    )
    got_up: time = Field(
        title="Время подъема",
        description="",
        examples=["13:00", "01:00"],
    )
    no_sleep: time = Field(
        default=time(hour=0, minute=0),
        title="Время отсутствия сна (в ЧЧ:ММ)",
        description="",
        examples=["00:00", "00:20"],
    )

    @computed_field(
        title="Длительность сна без учета времени отсутствия сна",
        return_type=timedelta,
    )
    @property
    @abc.abstractmethod
    def _sleep_duration_without_the_no_sleep(self: Self) -> timedelta: ...

    @computed_field(
        title="Длительность отсутствия сна (секунд)",
        return_type=timedelta,
    )
    @property
    @abc.abstractmethod
    def _no_sleep_duration(self: Self) -> timedelta: ...

    model_config: ConfigDict = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    def __eq__(self, other: Self) -> bool:
        return self.bedtime_date == other.bedtime_date

    def __hash__(self: Self) -> int:
        return hash(self.bedtime_date)
