from datetime import date, time

import pytest

from src.domain.values.points import Points
from tests.use_cases import (
    correct_points_4_different_order_of_sequences,
)


def test_points_in_can_create_no_sleep_field_by_default():
    points = Points(
        date(2020, 12, 12),
        time(1, 00),
        time(3, 00),
        time(11, 00),
        time(13, 00),
    )
    assert isinstance(points.no_sleep, time)
    assert points.no_sleep == time(0, 0)


@pytest.mark.parametrize(
    "correct_points",
    correct_points_4_different_order_of_sequences,
)
def test_create_points_with_different_first_point(
    correct_points: tuple[date, time, time, time, time],
):
    points = Points(*correct_points)
    assert points
    assert isinstance(points, Points)
    assert isinstance(points.bedtime_date, date)
    assert isinstance(points.went_to_bed, time)
    assert isinstance(points.fell_asleep, time)
    assert isinstance(points.woke_up, time)
    assert isinstance(points.got_up, time)
    assert isinstance(points.no_sleep, time)
