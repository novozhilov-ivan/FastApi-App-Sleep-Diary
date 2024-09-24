import operator

from dataclasses import dataclass, field
from typing_extensions import Self

from src.domain.services import NoteDurations
from src.domain.specifications.base import BaseSpecification


@dataclass
class NoSleepHasValidTime(BaseSpecification):
    durations: NoteDurations = field(init=False)

    def __post_init__(self: Self) -> None:
        self.durations: NoteDurations = NoteDurations(self.points)

    def __bool__(self: Self) -> bool:
        return operator.le(self.durations.without_sleep, self.durations.sleep)
