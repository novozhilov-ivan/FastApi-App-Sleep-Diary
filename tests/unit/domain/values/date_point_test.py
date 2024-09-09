from datetime import date, datetime
from typing import Any

import pytest

from src.domain.exceptions.date_point import (
    DatePointIsoFormatException,
    DatePointTypeException,
)
from src.domain.values.date_point import DatePoint


@pytest.mark.parametrize(
    "yyyymmdd",
    [
        date(2020, 1, 1),
        datetime(2020, 1, 1, 1, 1),
    ],
)
def test_create_date_point_from_date(yyyymmdd: datetime):
    time_point = DatePoint[date, date](yyyymmdd)
    assert isinstance(time_point.as_generic_type(), date)
    assert time_point.as_generic_type() == date(
        yyyymmdd.year,
        yyyymmdd.month,
        yyyymmdd.day,
    )


@pytest.mark.parametrize(
    "yyyymmdd",
    [
        "20200101",
        "2020-01-01",
    ],
)
def test_create_date_point_from_str_iso_format(yyyymmdd: str):
    time_point = DatePoint[str, date](yyyymmdd)
    assert isinstance(time_point.as_generic_type(), date)
    assert time_point.as_generic_type() == date(2020, 1, 1)


@pytest.mark.parametrize(
    "yyyymmdd",
    [
        20200101,
        ["2020:01:01"],
        [],
        {"2020": 101},
        {},
        (2020, "0101"),
        b"2020:01:01",
    ],
)
def test_create_date_point_from_forbidden_type(yyyymmdd: Any):
    with pytest.raises(DatePointTypeException):
        DatePoint(yyyymmdd)


@pytest.mark.parametrize(
    "yyyymmdd",
    [
        "202001",
        "20200101T101010",
        "2020-01-01T10:10:10",
        "20200101T101010+03",
        "20200101T10:10:10+03",
        "2020-01-01T10:10:10+03",
        "20200101T101010+0330",
        "2020-01-01T10:10:10+0330",
        "2020-01-01T10:10:10+03:30",
        "2020-01-01T10:10:10.100",
    ],
)
def test_create_date_point_from_forbidden_str_format(yyyymmdd: str):
    with pytest.raises(DatePointIsoFormatException):
        DatePoint(yyyymmdd)
