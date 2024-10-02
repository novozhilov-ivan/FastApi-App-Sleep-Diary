from dataclasses import dataclass, field
from datetime import date, time
from typing_extensions import Self

from src.domain.exceptions import (
    NoSleepDurationException,
    TimePointsSequenceException,
)
from src.domain.specifications import (
    NoSleepHasValidTime,
    PointsHasValidAnyAllowedSortedSequences,
)
from src.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Points(BaseValueObject):
    bedtime_date: date
    went_to_bed: time
    fell_asleep: time
    woke_up: time
    got_up: time
    no_sleep: time = field(default=time(0, 0))

    def validate(self: Self) -> None:
        if not NoSleepHasValidTime(self):
            raise NoSleepDurationException

        if not PointsHasValidAnyAllowedSortedSequences(self):
            raise TimePointsSequenceException
