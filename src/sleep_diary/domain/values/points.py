from dataclasses import dataclass
from datetime import date, time
from typing import Self

from src.sleep_diary.domain.exceptions import (
    NoSleepDurationException,
    TimePointsSequenceException,
)
from src.sleep_diary.domain.services import Durations
from src.sleep_diary.domain.specifications import (
    NoSleepHasValidTime,
    PointsHasValidAnyAllowedSortedSequences,
)
from src.sleep_diary.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class Points(BaseValueObject):
    bedtime_date: date
    went_to_bed: time
    fell_asleep: time
    woke_up: time
    got_up: time
    no_sleep: time = time()

    def validate(self: Self) -> None:
        if not NoSleepHasValidTime(Durations(self)):
            raise NoSleepDurationException

        if not PointsHasValidAnyAllowedSortedSequences(self):
            raise TimePointsSequenceException
