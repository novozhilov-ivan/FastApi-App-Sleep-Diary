from datetime import time, timedelta

from src.domain import note


def test_timedelta_with_hours_minutes_seconds_to_time() -> None:
    timedelta_test = timedelta(
        hours=1,
        minutes=25,
        seconds=45,
    )
    time_test = time(
        hour=1,
        minute=25,
    )
    time_from_timedelta = note.timedelta_seconds_to_time(td=timedelta_test)
    assert time_from_timedelta == time_test
    assert time_from_timedelta.hour == time_test.hour == 1
    assert time_from_timedelta.minute == time_test.minute == 25
    assert time_from_timedelta.second == time_test.second == 0


def test_timedelta_with_seconds_to_time() -> None:
    seconds_of_one_hour = 60 * 60
    seconds_of_twenty_five_minutes = 60 * 25
    useless_second_lesser_than_60 = 42
    test_seconds_value = (
        seconds_of_one_hour
        + seconds_of_twenty_five_minutes
        + useless_second_lesser_than_60
    )
    timedelta_test = timedelta(seconds=test_seconds_value)
    time_test = time(
        hour=1,
        minute=25,
    )
    time_from_timedelta = note.timedelta_seconds_to_time(td=timedelta_test)
    assert time_from_timedelta == time_test
    assert time_from_timedelta.hour == time_test.hour == 1
    assert time_from_timedelta.minute == time_test.minute == 25
    assert time_from_timedelta.second == time_test.second == 0
