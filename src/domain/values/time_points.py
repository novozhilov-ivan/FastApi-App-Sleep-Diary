from dataclasses import dataclass
from datetime import date, time
from typing_extensions import Self

from src.domain.exceptions import (
    TimePointsSequenceException,
)
from src.domain.specifications.duration import NoSleepHasValidTime
from src.domain.values.base import BaseValueObject
from src.domain.values.date_point import DatePoint
from src.domain.values.time_point import TimePoint


@dataclass(frozen=True)
class PointsIn:
    bedtime_date: DatePoint
    went_to_bed: TimePoint
    fell_asleep: TimePoint
    woke_up: TimePoint
    got_up: TimePoint
    no_sleep: TimePoint


@dataclass(frozen=True)
class PointsOut:
    bedtime_date: date
    went_to_bed: time
    fell_asleep: time
    woke_up: time
    got_up: time
    no_sleep: time


@dataclass(frozen=True)
class Points[
    VTI: PointsIn,
    VTO: PointsOut,
](BaseValueObject):
    def validate(self: Self) -> None:
        if not NoSleepHasValidTime(self):
            raise TimePointsSequenceException

        # if not AnyOfAllowedPointsSequences(self.as_generic_type()):
        #     raise NoSleepDurationException

    def as_generic_type(self: Self) -> PointsOut:
        return PointsOut(
            self.value.bedtime_date.as_generic_type(),
            self.value.went_to_bed.as_generic_type(),
            self.value.fell_asleep.as_generic_type(),
            self.value.woke_up.as_generic_type(),
            self.value.got_up.as_generic_type(),
            self.value.no_sleep.as_generic_type(),
        )
