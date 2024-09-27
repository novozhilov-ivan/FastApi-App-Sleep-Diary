import pytest

from src.domain.specifications import (
    WentToBedPointFirstInOrder,
)
from src.domain.values.points import PointsOut
from tests.unit.domain.conftest import wrong_points_where_wen_to_bed_is_wrong


@pytest.mark.parametrize(
    "wrong_points",
    wrong_points_where_wen_to_bed_is_wrong,
)
def test_sequence_where_went_to_bed_is_wrong(wrong_points: tuple):
    points_out = PointsOut(*wrong_points)
    assert bool(WentToBedPointFirstInOrder(points_out)) is False
