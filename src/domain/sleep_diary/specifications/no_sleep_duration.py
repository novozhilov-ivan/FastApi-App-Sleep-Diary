from dataclasses import dataclass
from operator import le

from src.domain.sleep_diary.services.base import IDurations
from src.domain.sleep_diary.specifications.base import BaseSpecification


@dataclass
class NoSleepHasValidTime(BaseSpecification):
    _durations: IDurations

    def _no_sleep_duration_le_sleep_duration(self) -> bool:
        return le(self._durations.without_sleep, self._durations.sleep)

    def __bool__(self) -> bool:
        return self._no_sleep_duration_le_sleep_duration()
