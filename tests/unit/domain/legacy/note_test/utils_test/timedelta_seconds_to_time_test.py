import datetime as dt

from src.domain import note as nt


def test_timedelta_with_hours_minutes_seconds_to_time() -> None:
    timedelta = dt.timedelta(
        hours=1,
        minutes=25,
        seconds=45,
    )
    time = dt.time(
        hour=1,
        minute=25,
    )
    time_from_timedelta = nt.timedelta_seconds_to_time(timedelta)
    assert time_from_timedelta == time
    assert time_from_timedelta.hour == time.hour == 1
    assert time_from_timedelta.minute == time.minute == 25
    assert time_from_timedelta.second == time.second == 0


def test_timedelta_with_seconds_to_time() -> None:
    seconds_of_one_hour = 60 * 60
    seconds_of_twenty_five_minutes = 60 * 25
    useless_second_lesser_than_60 = 42
    test_seconds_value = (
        seconds_of_one_hour
        + seconds_of_twenty_five_minutes
        + useless_second_lesser_than_60
    )
    timedelta = dt.timedelta(seconds=test_seconds_value)
    time = dt.time(
        hour=1,
        minute=25,
    )
    time_from_timedelta = nt.timedelta_seconds_to_time(timedelta)
    assert time_from_timedelta == time
    assert time_from_timedelta.hour == time.hour == 1
    assert time_from_timedelta.minute == time.minute == 25
    assert time_from_timedelta.second == time.second == 0
