import pytest

from src.domain.specifications import (
    FellAsleepPointFirstInOrder,
    GotUpPointFirstInOrder,
    PointsHasValidAnyAllowedSortedSequences,
    WentToBedPointFirstInOrder,
    WokUpPointFirstInOrder,
)
from tests.conftest import (
    all_wrong_points_sequences,
    wrong_points_where_fell_asleep_is_wrong,
    wrong_points_where_got_up_is_wrong,
    wrong_points_where_went_to_bed_is_wrong,
    wrong_points_where_woke_up_is_wrong,
)
from tests.unit.conftest import (
    FakePoints,
)


@pytest.mark.parametrize(
    "wrong_points",
    wrong_points_where_went_to_bed_is_wrong,
)
def test_sequence_where_went_to_bed_is_wrong(wrong_points: tuple):
    points = FakePoints(*wrong_points)
    specification = WentToBedPointFirstInOrder(points)
    assert not specification._is_sorted()
    assert bool(specification) is False
    assert not specification


@pytest.mark.parametrize(
    "wrong_points",
    wrong_points_where_fell_asleep_is_wrong,
)
def test_sequence_where_fell_asleep_is_wrong(wrong_points: tuple):
    points = FakePoints(*wrong_points)
    specification = FellAsleepPointFirstInOrder(points)
    assert not specification._is_sorted()
    assert bool(specification) is False
    assert not specification


@pytest.mark.parametrize(
    "wrong_points",
    wrong_points_where_woke_up_is_wrong,
)
def test_sequence_where_woke_up_is_wrong(wrong_points: tuple):
    points = FakePoints(*wrong_points)
    specification = WokUpPointFirstInOrder(points)
    assert not specification._is_sorted()
    assert bool(specification) is False
    assert not specification


@pytest.mark.parametrize(
    "wrong_points",
    wrong_points_where_got_up_is_wrong,
)
def test_sequence_where_got_up_is_wrong(wrong_points: tuple):
    points = FakePoints(*wrong_points)
    specification = GotUpPointFirstInOrder(points)
    assert not specification._is_sorted()
    assert bool(specification) is False
    assert not specification


@pytest.mark.parametrize(
    "wrong_points",
    all_wrong_points_sequences,
)
def test_sequence_all_time_point_can_be_wrong(wrong_points: tuple):
    points = FakePoints(*wrong_points)
    specification = PointsHasValidAnyAllowedSortedSequences(points)
    assert bool(specification) is False
    assert not specification
