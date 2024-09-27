from dataclasses import InitVar, dataclass, field
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
from src.domain.values.date_point import DatePoint
from src.domain.values.time_point import TimePoint


@dataclass(frozen=True)
class Points[
    VTDI: (str, date),
    VTTI: (str, time),
    VTDO: date,
    VTTO: time,
](BaseValueObject):
    value_bedtime_date: InitVar[VTDI] = field(repr=False)
    value_went_to_bed: InitVar[VTTI] = field(repr=False)
    value_fell_asleep: InitVar[VTTI] = field(repr=False)
    value_woke_up: InitVar[VTTI] = field(repr=False)
    value_got_up: InitVar[VTTI] = field(repr=False)
    value_no_sleep: InitVar[VTTI] = field(default="00:00", repr=False)

    bedtime_date: VTDO = field(init=False)
    went_to_bed: VTTO = field(init=False)
    fell_asleep: VTTO = field(init=False)
    woke_up: VTTO = field(init=False)
    got_up: VTTO = field(init=False)
    no_sleep: VTTO = field(init=False)

    def __post_init__(
        self: Self,
        value_bedtime_date: str | date,
        value_went_to_bed: str | time,
        value_fell_asleep: str | time,
        value_woke_up: str | time,
        value_got_up: str | time,
        value_no_sleep: str | time,
    ) -> None:
        object.__setattr__(
            self,
            "bedtime_date",
            DatePoint(value_bedtime_date).as_generic_type(),
        )
        object.__setattr__(
            self,
            "went_to_bed",
            TimePoint(value_went_to_bed).as_generic_type(),
        )
        object.__setattr__(
            self,
            "fell_asleep",
            TimePoint(value_fell_asleep).as_generic_type(),
        )
        object.__setattr__(
            self,
            "woke_up",
            TimePoint(value_woke_up).as_generic_type(),
        )
        object.__setattr__(
            self,
            "got_up",
            TimePoint(value_got_up).as_generic_type(),
        )
        object.__setattr__(
            self,
            "no_sleep",
            TimePoint(value_no_sleep).as_generic_type(),
        )
        super().__post_init__()

    def validate(self: Self) -> None:
        if not NoSleepHasValidTime(self):
            raise TimePointsSequenceException

        if not PointsHasValidAnyAllowedSortedSequences(self):
            raise NoSleepDurationException
