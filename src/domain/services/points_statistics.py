from dataclasses import dataclass
from datetime import time, timedelta
from operator import floordiv, mod, truediv
from typing_extensions import Self

from src.domain.services.base import BaseDurations, BaseStatistics


@dataclass
class Statistics(BaseStatistics):
    def __post_init__(self: Self, durations: BaseDurations) -> None:
        self.sleep = self._convert_timedelta_seconds_to_time(durations.sleep)
        self.in_bed = self._convert_timedelta_seconds_to_time(durations.in_bed)
        self.sleep_minus_no_sleep = self._convert_timedelta_seconds_to_time(
            durations.sleep_minus_without_sleep,
        )
        self.sleep_efficiency = self._compute_efficiency(
            durations.sleep_minus_without_sleep,
            durations.in_bed,
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
