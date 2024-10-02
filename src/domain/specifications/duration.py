from dataclasses import dataclass, field
from operator import le
from typing_extensions import Self

from src.domain.services import Durations
from src.domain.specifications.base import BaseSpecification


@dataclass
class NoSleepHasValidTime(BaseSpecification):
    durations: Durations = field(init=False)

    def __post_init__(self: Self) -> None:
        self.durations: Durations = Durations(self.points)

    def no_sleep_duration_le_sleep_duration(self: Self) -> bool:
        return le(self.durations.without_sleep, self.durations.sleep)

    def __bool__(self: Self) -> bool:
        return self.no_sleep_duration_le_sleep_duration()
