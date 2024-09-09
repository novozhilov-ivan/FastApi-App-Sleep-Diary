import abc

from dataclasses import dataclass
from datetime import time
from typing import Generic, TypeVar
from typing_extensions import Self


TimePointTypeIn = TypeVar("TimePointTypeIn", str, time)
TimePointTypeOut = TypeVar("TimePointTypeOut", bound=time)


@dataclass(eq=False)
class TimePointException(Exception):
    @property
    def message(self: Self) -> str:
        return "Ошибка создания time point."


@dataclass(frozen=True)
class BaseValueObject(abc.ABC, Generic[TimePointTypeIn, TimePointTypeOut]):
    def __init__(self: Self, value: TimePointTypeIn) -> None:
        self.value: TimePointTypeOut
        if isinstance(value, str):
            try:
                self.value = time.fromisoformat(value)
            except ValueError:
                raise TimePointException
        else:
            self.value = time(value.hour, value.minute)

    def __post_init__(self: Self) -> None:
        self.value.replace(second=0, microsecond=0, tzinfo=None)
        self.validate()

    @abc.abstractmethod
    def validate(self: Self) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class TimePoint(BaseValueObject[TimePointTypeIn, TimePointTypeOut]):

    def validate(self: Self) -> None: ...
