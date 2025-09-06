from dataclasses import dataclass
from datetime import time

from src.domain.sleep_diary.services.base import IDurations, IStatistics


@dataclass
class WeekStatistics(IStatistics):
    durations: list[IDurations]

    @property
    def sleep(self) -> time:
        raise NotImplementedError

    @property
    def in_bed(self) -> time:
        raise NotImplementedError

    @property
    def sleep_minus_no_sleep(self) -> time:
        raise NotImplementedError

    @property
    def sleep_efficiency(self) -> float:
        raise NotImplementedError
