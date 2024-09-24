from abc import ABC, abstractmethod
from datetime import time
from typing_extensions import Self

from more_itertools import is_sorted

from src.domain.specifications.base import BaseSpecification


class PointsSequenceIsSortedAsc(BaseSpecification, ABC):
    """
    True если каждая временная точка из последовательности меньше или равна
    следующей.
    """

    @abstractmethod
    def sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        raise NotImplementedError

    def __bool__(self: Self) -> bool:
        return is_sorted(self.sequence_of_points())


class WentToBedPointFirstInOrder(PointsSequenceIsSortedAsc):
    def sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self.points.went_to_bed,
            self.points.fell_asleep,
            self.points.woke_up,
            self.points.got_up,
        )


class GotUpPointFirstInOrder(PointsSequenceIsSortedAsc):
    def sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self.points.got_up,
            self.points.went_to_bed,
            self.points.fell_asleep,
            self.points.woke_up,
        )


class WokUpPointFirstInOrder(PointsSequenceIsSortedAsc):
    def sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self.points.woke_up,
            self.points.got_up,
            self.points.went_to_bed,
            self.points.fell_asleep,
        )


class FellAsleepPointFirstInOrder(PointsSequenceIsSortedAsc):
    def sequence_of_points(self: Self) -> tuple[time, time, time, time]:
        return (
            self.points.fell_asleep,
            self.points.woke_up,
            self.points.got_up,
            self.points.went_to_bed,
        )


class PointsHasValidAnyAllowedSortedSequences(BaseSpecification):
    def __bool__(self: Self) -> bool:
        return any(
            (
                WentToBedPointFirstInOrder(self.points),
                GotUpPointFirstInOrder(self.points),
                WokUpPointFirstInOrder(self.points),
                FellAsleepPointFirstInOrder(self.points),
            ),
        )
