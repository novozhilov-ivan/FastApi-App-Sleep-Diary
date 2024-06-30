import abc

from datetime import (
    date,
    time,
    timedelta,
)
from typing import (
    Annotated,
    ClassVar,
)
from typing_extensions import Self

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
)

from src.domain.note.utils import normalize_str_to_date, normalize_str_to_time


StrToTime = Annotated[time | str, AfterValidator(normalize_str_to_time)]
StrToDate = Annotated[date | str, AfterValidator(normalize_str_to_date)]


class NoteBase(BaseModel, abc.ABC):
    bedtime_date: StrToDate = Field(
        title="Дата отхода ко сну",
        description="",
        examples=["2020-12-12", "2021-01-20"],
    )
    went_to_bed: StrToTime = Field(
        title="Время отхода ко сну",
        description="",
        examples=["01:00", "13:00"],
    )
    fell_asleep: StrToTime = Field(
        title="Время засыпания",
        description="",
        examples=["03:00", "15:00"],
    )
    woke_up: StrToTime = Field(
        title="Время пробуждения",
        description="",
        examples=["11:00", "23:00"],
    )
    got_up: StrToTime = Field(
        title="Время подъема",
        description="",
        examples=["13:00", "01:00"],
    )
    no_sleep: StrToTime = Field(
        default=time(hour=0, minute=0),
        title="Время отсутствия сна (в ЧЧ:ММ)",
        description="",
        examples=["00:00", "00:20"],
    )

    @computed_field(  # type: ignore[misc]
        title="Длительность сна без учета времени отсутствия сна",
        return_type=timedelta,
    )
    @property
    @abc.abstractmethod
    def _sleep_duration_without_no_sleep(self: Self) -> timedelta: ...

    @computed_field(  # type: ignore[misc]
        title="Длительность времени, проведенного в постели.",
        return_type=timedelta,
    )
    @property
    @abc.abstractmethod
    def _spent_in_bed_duration(self: Self) -> timedelta: ...

    @computed_field(  # type: ignore[misc]
        title="Длительность отсутствия сна (секунд)",
        return_type=timedelta,
    )
    @property
    @abc.abstractmethod
    def _no_sleep_duration(self: Self) -> timedelta: ...

    model_config: ClassVar[ConfigDict] = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    def __eq__(self: Self, other: object) -> bool:
        if not isinstance(other, NoteBase):
            return NotImplemented
        return self.bedtime_date == other.bedtime_date

    def __hash__(self: Self) -> int:
        return hash(self.bedtime_date)
