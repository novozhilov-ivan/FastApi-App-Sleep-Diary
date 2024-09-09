import datetime

from datetime import time
from typing import Any

import pytest

from src.domain.exceptions.time_point import (
    TimePointFormatIsoException,
    TimePointTypeException,
)
from src.domain.values.time_point import TimePoint


def test_create_time_point_from_time():
    hhmm = time(1, 1)
    time_point = TimePoint[time, time](hhmm)
    assert isinstance(time_point.as_generic_type(), time)
    assert time_point.as_generic_type() == time(1, 1, 0, 0, None)


@pytest.mark.parametrize(
    "hhmm",
    [
        "1010",
        "10:10",
        "101010",
        "10:10:10",
        "10:10:10:101010",
        "101010+03",
        "10:10:10+03:30",
    ],
)
def test_create_time_point_from_str_iso_format(hhmm: str):
    time_point = TimePoint[str, time](hhmm)
    assert isinstance(time_point.as_generic_type(), time)
    assert time_point.as_generic_type() == time(10, 10, 0, 0, None)


@pytest.mark.parametrize(
    "hhmm",
    [
        1010,
        ["10:10"],
        [],
        {"10": 10},
        {},
        (10, "10"),
        b"10:10",
        datetime.datetime(2020, 1, 1, 1, 1),
    ],
)
def test_create_time_point_from_forbidden_type(hhmm: Any):
    with pytest.raises(TimePointTypeException):
        TimePoint(hhmm)


@pytest.mark.parametrize(
    "hhmm",
    [
        "24:00",
        "23:66",
        "+10",
        "+1010",
        "+10:10",
    ],
)
def test_create_time_point_from_forbidden_str_format(hhmm: str):
    with pytest.raises(TimePointFormatIsoException):
        TimePoint(hhmm)
