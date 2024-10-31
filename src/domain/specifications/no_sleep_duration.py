from dataclasses import dataclass
from operator import le
from typing_extensions import Self

from src.domain.services import IDurations
from src.domain.specifications.base import BaseSpecification


@dataclass
class NoSleepHasValidTime(BaseSpecification):
    _durations: IDurations

    def _no_sleep_duration_le_sleep_duration(self: Self) -> bool:
        return le(self._durations.without_sleep, self._durations.sleep)

    def __bool__(self: Self) -> bool:
        return self._no_sleep_duration_le_sleep_duration()
