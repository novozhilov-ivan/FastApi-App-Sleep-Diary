from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import time
from typing_extensions import Self

from more_itertools import is_sorted

from src.domain.specifications.base import BasePointsSpecification


@dataclass
class PointsSequenceIsSortedAsc(BasePointsSpecification, ABC):
    """
    True если каждая временная точка из последовательности меньше или равна
    следующей.
    """

    @abstractmethod
    def sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        raise NotImplementedError

    def is_sorted(self: Self) -> bool:
        return is_sorted(self.sequence_of_points())

    def __bool__(self: Self) -> bool:
        return self.is_sorted()


@dataclass
class WentToBedPointFirstInOrder(PointsSequenceIsSortedAsc):
    def sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self.points.went_to_bed,
            self.points.fell_asleep,
            self.points.woke_up,
            self.points.got_up,
        )


@dataclass
class FellAsleepPointFirstInOrder(PointsSequenceIsSortedAsc):
    def sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self.points.fell_asleep,
            self.points.woke_up,
            self.points.got_up,
            self.points.went_to_bed,
        )


@dataclass
class WokUpPointFirstInOrder(PointsSequenceIsSortedAsc):
    def sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self.points.woke_up,
            self.points.got_up,
            self.points.went_to_bed,
            self.points.fell_asleep,
        )


@dataclass
class GotUpPointFirstInOrder(PointsSequenceIsSortedAsc):
    def sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self.points.got_up,
            self.points.went_to_bed,
            self.points.fell_asleep,
            self.points.woke_up,
        )


@dataclass(eq=True)
class PointsHasValidAnyAllowedSortedSequences(BasePointsSpecification):
    def __bool__(self: Self) -> bool:
        return any(
            (
                WentToBedPointFirstInOrder(self.points),
                GotUpPointFirstInOrder(self.points),
                WokUpPointFirstInOrder(self.points),
                FellAsleepPointFirstInOrder(self.points),
            ),
        )
