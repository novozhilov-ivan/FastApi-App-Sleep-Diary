from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import time
from typing import Self, TYPE_CHECKING

from more_itertools import is_sorted

from src.sleep_diary.domain.specifications.base import BaseSpecification


if TYPE_CHECKING:
    from src.sleep_diary.domain.values.points import Points


@dataclass
class PointsSpecification(BaseSpecification, ABC):
    _points: "Points"


@dataclass
class PointsSequenceIsSortedAsc(PointsSpecification, ABC):
    """
    True если каждая временная точка из последовательности меньше или равна
    следующей.
    """

    @abstractmethod
    def _sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        raise NotImplementedError

    def _is_sorted(self: Self) -> bool:
        return is_sorted(self._sequence_of_points())

    def __bool__(self: Self) -> bool:
        return self._is_sorted()


@dataclass
class WentToBedPointFirstInOrder(PointsSequenceIsSortedAsc):
    def _sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self._points.went_to_bed,
            self._points.fell_asleep,
            self._points.woke_up,
            self._points.got_up,
        )


@dataclass
class FellAsleepPointFirstInOrder(PointsSequenceIsSortedAsc):
    def _sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self._points.fell_asleep,
            self._points.woke_up,
            self._points.got_up,
            self._points.went_to_bed,
        )


@dataclass
class WokUpPointFirstInOrder(PointsSequenceIsSortedAsc):
    def _sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self._points.woke_up,
            self._points.got_up,
            self._points.went_to_bed,
            self._points.fell_asleep,
        )


@dataclass
class GotUpPointFirstInOrder(PointsSequenceIsSortedAsc):
    def _sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self._points.got_up,
            self._points.went_to_bed,
            self._points.fell_asleep,
            self._points.woke_up,
        )


@dataclass
class PointsHasValidAnyAllowedSortedSequences(PointsSpecification):
    def __bool__(self: Self) -> bool:
        return any(
            (
                WentToBedPointFirstInOrder(self._points),
                GotUpPointFirstInOrder(self._points),
                WokUpPointFirstInOrder(self._points),
                FellAsleepPointFirstInOrder(self._points),
            ),
        )
