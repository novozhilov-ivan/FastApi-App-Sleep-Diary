from typing_extensions import Self

import pytest

from src.domain.specifications import (
    WentToBedPointFirstInOrder,
)
from src.domain.values.points import Points
from tests.unit.domain.conftest import wrong_points_ins_where_wen_to_bed_is_wrong


class FakePoints(Points):
    def validate(self: Self) -> None: ...


@pytest.mark.parametrize(
    "wrong_points_in",
    wrong_points_ins_where_wen_to_bed_is_wrong,
)
def test_sequence_where_went_to_bed_is_wrong(wrong_points_in: tuple):
    points_out = FakePoints(*wrong_points_in)
    assert bool(WentToBedPointFirstInOrder(points_out)) is False
