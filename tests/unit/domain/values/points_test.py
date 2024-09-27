from datetime import date, time

import pytest

from src.domain.values.points import Points
from tests.unit.domain.conftest import (
    correct_points_ins_4_different_order_of_sequences,
    points_in_with_went_to_bed_is_first,
)


def test_points_in_can_create_no_sleep_field_by_default():
    points = Points[str, str, date, time](
        "2020-12-12",
        "01:00",
        "03:00",
        "11:00",
        "13:00",
    )
    assert isinstance(points.no_sleep, time)
    assert points.no_sleep == time(0, 0)


@pytest.mark.parametrize(
    "points_in",
    correct_points_ins_4_different_order_of_sequences,
)
def test_create_points_with_different_first_point(
    points_in: tuple[str, str, str, str, str],
):
    points = Points[str, str, date, time](*points_in)
    assert points
    assert isinstance(points, Points)


def test_points_as_generic_type_returned_type_fields_of_points():
    points = Points[str, str, date, time](*points_in_with_went_to_bed_is_first)

    assert isinstance(points, Points)
    assert isinstance(points.bedtime_date, date)
    assert isinstance(points.went_to_bed, time)
    assert isinstance(points.fell_asleep, time)
    assert isinstance(points.woke_up, time)
    assert isinstance(points.got_up, time)
    assert isinstance(points.no_sleep, time)
