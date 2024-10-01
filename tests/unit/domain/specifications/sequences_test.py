from typing_extensions import Self

import pytest

from src.domain.specifications import (
    FellAsleepPointFirstInOrder,
    GotUpPointFirstInOrder,
    PointsHasValidAnyAllowedSortedSequences,
    WentToBedPointFirstInOrder,
    WokUpPointFirstInOrder,
)
from src.domain.values.points import Points
from tests.unit.domain.conftest import (
    all_wrong_points_sequences,
    wrong_points_where_fell_asleep_is_wrong,
    wrong_points_where_got_up_is_wrong,
    wrong_points_where_went_to_bed_is_wrong,
    wrong_points_where_woke_up_is_wrong,
)


class FakePoints(Points):
    def validate(self: Self) -> None: ...


@pytest.mark.parametrize(
    "wrong_points",
    wrong_points_where_went_to_bed_is_wrong,
)
def test_sequence_where_went_to_bed_is_wrong(wrong_points: tuple):
    points_out = FakePoints(*wrong_points)
    specification = WentToBedPointFirstInOrder(points_out)
    assert not specification.is_sorted()
    assert bool(specification) is False
    assert not specification


@pytest.mark.parametrize(
    "wrong_points",
    wrong_points_where_fell_asleep_is_wrong,
)
def test_sequence_where_fell_asleep_is_wrong(wrong_points: tuple):
    points_out = FakePoints(*wrong_points)
    specification = FellAsleepPointFirstInOrder(points_out)
    assert not specification.is_sorted()
    assert bool(specification) is False
    assert not specification


@pytest.mark.parametrize(
    "wrong_points",
    wrong_points_where_woke_up_is_wrong,
)
def test_sequence_where_woke_up_is_wrong(wrong_points: tuple):
    points_out = FakePoints(*wrong_points)
    specification = WokUpPointFirstInOrder(points_out)
    assert not specification.is_sorted()
    assert bool(specification) is False
    assert not specification


@pytest.mark.parametrize(
    "wrong_points",
    wrong_points_where_got_up_is_wrong,
)
def test_sequence_where_got_up_is_wrong(wrong_points: tuple):
    points_out = FakePoints(*wrong_points)
    specification = GotUpPointFirstInOrder(points_out)
    assert not specification.is_sorted()
    assert bool(specification) is False
    assert not specification


@pytest.mark.parametrize(
    "wrong_points",
    all_wrong_points_sequences,
)
def test_sequence_all_time_point_can_be_wrong(wrong_points: tuple):
    points_out = FakePoints(*wrong_points)
    specification = PointsHasValidAnyAllowedSortedSequences(points_out)
    assert bool(specification) is False
    assert not specification
