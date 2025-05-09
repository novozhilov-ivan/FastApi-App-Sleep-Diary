from dataclasses import dataclass
from datetime import time, timedelta
from operator import floordiv, mod, truediv
from typing import Self

from src.sleep_diary.domain.services import IStatistics


@dataclass
class Statistics(IStatistics):
    @property
    def sleep(self: Self) -> time:
        return self._convert_timedelta_seconds_to_time(self.durations.sleep)

    @property
    def in_bed(self: Self) -> time:
        return self._convert_timedelta_seconds_to_time(self.durations.in_bed)

    @property
    def sleep_minus_no_sleep(self: Self) -> time:
        return self._convert_timedelta_seconds_to_time(
            self.durations.sleep_minus_without_sleep,
        )

    @property
    def sleep_efficiency(self: Self) -> float:
        return self._compute_efficiency(
            self.durations.sleep_minus_without_sleep,
            self.durations.in_bed,
        )

    @staticmethod
    def _convert_timedelta_seconds_to_time(value: timedelta) -> time:
        return time(
            hour=floordiv(value.seconds, 60 * 60),
            minute=mod(floordiv(value.seconds, 60), 60),
        )

    @staticmethod
    def _compute_efficiency(
        small_duration: timedelta,
        bid_duration: timedelta,
    ) -> float:
        if bid_duration == timedelta():
            return 0.0
        return round(
            number=truediv(small_duration, bid_duration),
            ndigits=2,
        )
