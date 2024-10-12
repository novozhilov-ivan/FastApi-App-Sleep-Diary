from dataclasses import dataclass
from operator import le
from typing_extensions import Self

from src.domain.services.base import BaseDurations
from src.domain.specifications.base import BaseSpecification


@dataclass
class NoSleepHasValidTime(BaseSpecification):
    durations: BaseDurations

    def no_sleep_duration_le_sleep_duration(self: Self) -> bool:
        return le(self.durations.without_sleep, self.durations.sleep)

    def __bool__(self: Self) -> bool:
        return self.no_sleep_duration_le_sleep_duration()
