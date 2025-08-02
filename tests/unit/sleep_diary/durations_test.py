from datetime import time, timedelta

import pytest

from src.domain.sleep_diary.services.durations import Durations
from tests.conftest import (
    correct_points_4_different_order_of_sequences,
)
from tests.unit.sleep_diary.conftest import FakePoints


@pytest.mark.parametrize(
    "no_sleep",
    [
        time(),
        time(1),
    ],
)
@pytest.mark.parametrize(
    "points_in",
    correct_points_4_different_order_of_sequences,
)
def test_points_durations(points_in: tuple, no_sleep: time) -> None:
    date_and_times_with_no_sleep: tuple = (*points_in, no_sleep)
    points = FakePoints(*date_and_times_with_no_sleep)
    durations = Durations(points)
    assert durations.sleep == timedelta(hours=8)
    assert durations.in_bed == timedelta(hours=12)
    assert durations.without_sleep == timedelta(hours=(0 + no_sleep.hour))
    assert durations.sleep_minus_without_sleep == timedelta(
        hours=(8 - no_sleep.hour),
    )


@pytest.mark.parametrize(
    "points_in",
    correct_points_4_different_order_of_sequences,
)
def test_durations_where_no_sleep_cannot_be_gt_sleep_and_cannot_be_lt_zero(
    points_in: tuple,
) -> None:
    nine_hours_of_no_sleep = time(9)
    date_and_times_with_no_sleep: tuple = (*points_in, nine_hours_of_no_sleep)
    points = FakePoints(*date_and_times_with_no_sleep)
    durations = Durations(points)

    assert durations.sleep == timedelta(hours=8)
    assert durations.in_bed == timedelta(hours=12)
    assert durations.without_sleep == timedelta(hours=9)
    assert durations.sleep_minus_without_sleep == timedelta(hours=0)
