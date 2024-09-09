from dataclasses import dataclass
from datetime import time
from typing_extensions import Self

from src.domain.exceptions.time_point import (
    TimePointFormatIsoException,
    TimePointTypeException,
)
from src.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class TimePoint[VTI: str | time, VTO: time](BaseValueObject):
    def validate(self: Self) -> None:
        if not isinstance(self.value, (time, str)):
            raise TimePointTypeException

        if isinstance(self.value, str):
            try:
                time.fromisoformat(self.value)
            except ValueError:
                raise TimePointFormatIsoException

    def as_generic_type(self: Self) -> time:
        if isinstance(self.value, str):
            return time.fromisoformat(self.value).replace(
                second=0,
                microsecond=0,
                tzinfo=None,
            )
        return time(self.value.hour, self.value.minute)
