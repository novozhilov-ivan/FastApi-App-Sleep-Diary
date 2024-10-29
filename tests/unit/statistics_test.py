from datetime import time, timedelta
from operator import truediv

import pytest

from src.domain.entities import IStatistics
from src.domain.services import Durations, Statistics
from src.domain.values.points import Points
from tests.unit.conftest import FakePoints
from tests.use_cases import (
    correct_points_4_different_order_of_sequences_and_one_hour_no_sleep,
    date_point,
    points_all_zero,
    points_with_zeros_and_some_big_no_sleep,
)


@pytest.mark.parametrize(
    "points_in",
    [
        points_all_zero,
        points_with_zeros_and_some_big_no_sleep,
    ],
)
def test_statistics_with_all_zero_points(points_in: tuple):
    points = FakePoints(*points_in)
    statistics_: IStatistics = Statistics(Durations(points))

    assert statistics_.sleep == time()
    assert statistics_.in_bed == time()
    assert statistics_.sleep_minus_no_sleep == time()
    assert statistics_.sleep_efficiency == 0.0


def test_note_statistic_some_correct_points():
    points = Points(
        date_point,
        time(1, 25),
        time(1, 45),
        time(9, 53),
        time(10, 9),
        time(0, 11),
    )
    statistics_: IStatistics = Statistics(Durations(points))

    assert statistics_.sleep == time(hour=8, minute=8)
    assert statistics_.in_bed == time(hour=8, minute=44)
    assert statistics_.sleep_minus_no_sleep == time(hour=7, minute=57)
    assert statistics_.sleep_efficiency == round(
        number=truediv(
            (7 * 60 + 57),
            (8 * 60 + 46),
        ),
        ndigits=2,
    )


@pytest.mark.parametrize(
    "points_in",
    correct_points_4_different_order_of_sequences_and_one_hour_no_sleep,
)
def test_statistics_of_correct_points_with_different_order_and_same_durations(
    points_in: tuple,
):
    points = Points(*points_in)
    statistics_: IStatistics = Statistics(Durations(points))

    assert statistics_.sleep == time(8)
    assert statistics_.in_bed == time(12)
    assert statistics_.sleep_minus_no_sleep == time(7)
    assert statistics_.sleep_efficiency == 0.58


def test_timedelta_with_hours_minutes_seconds_to_time():
    timedelta_to_convert = timedelta(hours=1, minutes=25, seconds=45)
    time_from_timedelta = Statistics._convert_timedelta_seconds_to_time(
        timedelta_to_convert,
    )

    expected_time = time(1, 25)

    assert time_from_timedelta == expected_time
    assert time_from_timedelta.hour == expected_time.hour == 1
    assert time_from_timedelta.minute == expected_time.minute == 25
    assert time_from_timedelta.second == expected_time.second == 0


def test_timedelta_with_seconds_to_time():
    seconds_of_one_hour = 60 * 60
    seconds_of_twenty_five_minutes = 60 * 25
    useless_second_lesser_than_60 = 42
    test_seconds_value = sum(
        (
            seconds_of_one_hour,
            seconds_of_twenty_five_minutes,
            useless_second_lesser_than_60,
        ),
    )
    timedelta_to_convert = timedelta(seconds=test_seconds_value)
    time_from_timedelta = Statistics._convert_timedelta_seconds_to_time(
        timedelta_to_convert,
    )

    expected_time = time(1, 25)

    assert time_from_timedelta == expected_time
    assert time_from_timedelta.hour == expected_time.hour == 1
    assert time_from_timedelta.minute == expected_time.minute == 25
    assert time_from_timedelta.second == expected_time.second == 0


@pytest.mark.parametrize(
    ("small_duration", "bid_duration", "expected_result"),
    [
        (timedelta(), timedelta(), 0.0),
        (timedelta(10), timedelta(), 0.0),
        (timedelta(hours=5), timedelta(hours=10), 0.5),
        (timedelta(minutes=5), timedelta(minutes=10), 0.5),
        (timedelta(7), timedelta(12), 0.58),
    ],
)
def test_computing_sleep_efficiency(
    small_duration: timedelta,
    bid_duration: timedelta,
    expected_result: float,
):
    efficiency = Statistics._compute_efficiency(small_duration, bid_duration)

    assert efficiency == expected_result
