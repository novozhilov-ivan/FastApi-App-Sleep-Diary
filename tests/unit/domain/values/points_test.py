from datetime import date, time

import pytest

from src.domain.values import DatePoint, Points, PointsIn, PointsOut, TimePoint
from tests.unit.domain.values.conftest import (
    points_in_with_fell_asleep_is_first,
    points_in_with_got_up_is_first,
    points_in_with_went_to_bed_is_first,
    points_in_with_woke_up_is_first,
)


def test_points_in_can_create_no_sleep_field_by_default():
    points = PointsIn(
        bedtime_date=DatePoint("2020-12-12"),
        went_to_bed=TimePoint("01:00"),
        fell_asleep=TimePoint("03:00"),
        woke_up=TimePoint("11:00"),
        got_up=TimePoint("13:00"),
    )
    no_sleep = points.no_sleep.as_generic_type()
    assert isinstance(no_sleep, time)
    assert no_sleep == time(0, 0)


@pytest.mark.parametrize(
    "points_in",
    [
        points_in_with_went_to_bed_is_first,
        points_in_with_got_up_is_first,
        points_in_with_woke_up_is_first,
        points_in_with_fell_asleep_is_first,
    ],
)
def test_create_points_with_different_first_point(points_in: PointsIn):
    points = Points[PointsIn, PointsOut](points_in)
    assert points
    assert points.value
    assert isinstance(points.value, PointsIn)
    assert isinstance(points.as_generic_type(), PointsOut)


def test_points_as_generic_type_returned_type_fields_of_points():
    points = Points[PointsIn, PointsOut](points_in_with_went_to_bed_is_first)
    points_out: PointsOut = points.as_generic_type()

    assert isinstance(points_out, PointsOut)
    assert isinstance(points_out.bedtime_date, date)
    assert isinstance(points_out.went_to_bed, time)
    assert isinstance(points_out.fell_asleep, time)
    assert isinstance(points_out.woke_up, time)
    assert isinstance(points_out.got_up, time)
    assert isinstance(points_out.no_sleep, time)
