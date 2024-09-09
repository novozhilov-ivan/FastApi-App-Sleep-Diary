from dataclasses import dataclass
from datetime import time
from typing_extensions import Self

from src.domain.exceptions.time_point import (
    TimePointFormatException,
    TimePointTypeException,
)
from src.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class TimePoint[VTI: str | time, VTO: time](BaseValueObject):
    def validate(self: Self) -> None:
        if isinstance(self.value, time):
            return
        if isinstance(self.value, str):
            try:
                time.fromisoformat(self.value)
            except ValueError:
                raise TimePointFormatException
        else:
            raise TimePointTypeException

    def as_generic_type(self: Self) -> time:
        if isinstance(self.value, str):
            return time.fromisoformat(self.value).replace(
                second=0,
                microsecond=0,
                tzinfo=None,
            )
        return time(self.value.hour, self.value.minute)
