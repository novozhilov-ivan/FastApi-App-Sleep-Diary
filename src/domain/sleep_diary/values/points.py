from dataclasses import dataclass
from datetime import date, time

from src.domain.sleep_diary.exceptions.note import (
    NoSleepDurationException,
    TimePointsSequenceException,
)
from src.domain.sleep_diary.services.durations import Durations
from src.domain.sleep_diary.specifications.no_sleep_duration import (
    NoSleepHasValidTime,
)
from src.domain.sleep_diary.specifications.sequences import (
    PointsHasValidAnyAllowedSortedSequences,
)
from src.domain.sleep_diary.values.base import BaseValueObject


@dataclass(frozen=True)
class Points(BaseValueObject):
    bedtime_date: date
    went_to_bed: time
    fell_asleep: time
    woke_up: time
    got_up: time
    no_sleep: time = time()

    def validate(self) -> None:
        if not NoSleepHasValidTime(Durations(self)):
            raise NoSleepDurationException

        if not PointsHasValidAnyAllowedSortedSequences(self):
            raise TimePointsSequenceException
