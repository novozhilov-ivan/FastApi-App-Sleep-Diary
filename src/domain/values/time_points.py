from dataclasses import dataclass
from datetime import date, time
from typing_extensions import Self

from src.domain.values.base import BaseValueObject


@dataclass
class TimePointsIn:
    bedtime_date: date | str
    went_to_bed: time | str
    fell_asleep: time | str
    woke_up: time | str
    got_up: time | str
    no_sleep: time | str


@dataclass
class TimePointsOut:
    bedtime_date: date
    went_to_bed: time
    fell_asleep: time
    woke_up: time
    got_up: time
    no_sleep: time


@dataclass(frozen=True)
class TimePoints[
    VTI: TimePointsIn,
    VTO: TimePointsOut,
](BaseValueObject):
    def validate(self: Self) -> None:
        # specs(self)
        ...

    def as_generic_type(self: Self) -> TimePointsOut:
        return TimePointsOut(
            self.value.bedtime_date,
            self.value.went_to_bed,
            self.value.fell_asleep,
            self.value.woke_up,
            self.value.got_up,
            self.value.no_sleep,
        )
