import abc
import datetime as dt

from typing_extensions import Self

from pydantic import (
    BaseModel,
    Field,
    computed_field,
    model_validator,
)


class BaseNoteDateTimePoints(BaseModel, abc.ABC):
    bedtime_date: dt.date = Field(
        title="Дата отхода ко сну",
        description="",
        examples=["2020-12-12", "2021-01-20"],
    )
    went_to_bed: dt.time = Field(
        title="Время отхода ко сну",
        description="",
        examples=["01:00", "13:00"],
    )
    fell_asleep: dt.time = Field(
        title="Время засыпания",
        description="",
        examples=["03:00", "15:00"],
    )
    woke_up: dt.time = Field(
        title="Время пробуждения",
        description="",
        examples=["11:00", "23:00"],
    )
    got_up: dt.time = Field(
        title="Время подъема",
        description="",
        examples=["13:00", "01:00"],
    )
    no_sleep: dt.time = Field(
        default=dt.time(hour=0, minute=0),
        title="Время отсутствия сна",
        description="",
        examples=["00:00", "00:20"],
    )


class BaseTimePointsSequencesValidator(BaseNoteDateTimePoints, abc.ABC):
    @model_validator(mode="after")
    @abc.abstractmethod
    def validate_time_points_sequences(self: Self) -> Self: ...


class BaseNoteDurations(BaseNoteDateTimePoints, abc.ABC):
    @computed_field(title="Длительность сна")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def _sleep_duration(self: Self) -> dt.timedelta: ...

    @computed_field(  # type: ignore[misc]
        title="Длительность сна за вычетом времени без сна",
    )
    @property
    @abc.abstractmethod
    def _sleep_duration_minus_no_sleep(self: Self) -> dt.timedelta: ...

    @computed_field(  # type: ignore[misc]
        title="Длительность времени, проведенного в постели.",
    )
    @property
    @abc.abstractmethod
    def _in_bed_duration(self: Self) -> dt.timedelta: ...

    @computed_field(title="Длительность отсутствия сна")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def _no_sleep_duration(self: Self) -> dt.timedelta: ...


class BaseNoSleepDurationValidator(BaseNoteDurations, abc.ABC):
    @model_validator(mode="after")
    @abc.abstractmethod
    def validate_no_sleep_duration(self: Self) -> Self: ...


class BaseNoteStatistic(BaseNoteDurations, abc.ABC):
    @computed_field(title="Время сна")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def time_in_sleep(self: Self) -> dt.time: ...

    @computed_field(title="Время в кровати")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def time_in_bed(self: Self) -> dt.time: ...

    @computed_field(  # type: ignore[misc]
        title="Время сна за вычетом времени без сна",
    )
    @property
    @abc.abstractmethod
    def time_in_sleep_minus_no_sleep(self: Self) -> dt.time: ...

    @computed_field(title="Эффективность сна (%)")  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def sleep_efficiency(self: Self) -> float: ...


class BaseNoteValueObject(
    BaseNoteStatistic,
    BaseTimePointsSequencesValidator,
    BaseNoSleepDurationValidator,
    BaseNoteDateTimePoints,
    abc.ABC,
):
    @abc.abstractmethod
    def __eq__(self: Self, other: object) -> bool: ...

    @abc.abstractmethod
    def __hash__(self: Self) -> int: ...


class BaseNoteEntity(BaseNoteValueObject, abc.ABC):
    oid: int = Field(gt=0)
    created_at: dt.datetime
    updated_at: dt.datetime
