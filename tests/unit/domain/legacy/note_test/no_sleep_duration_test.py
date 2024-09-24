import pytest

from src.domain.exceptions import NoSleepDurationException
from src.domain.note import NoteTimePoints


def test_no_sleep_time_cannot_be_gt_sleep_time_with_increases_time_points():
    with pytest.raises(NoSleepDurationException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="01:00",
            fell_asleep="03:00",
            woke_up="11:00",
            got_up="13:00",
            no_sleep="09:00",
        )


def test_no_sleep_time_cannot_be_gt_sleep_time_with_one_time_points_after_midnight():  # noqa
    with pytest.raises(NoSleepDurationException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="13:00",
            fell_asleep="15:00",
            woke_up="23:00",
            got_up="01:00",
            no_sleep="09:00",
        )


def test_no_sleep_time_cannot_be_gt_sleep_time_with_two_time_points_after_midnight():  # noqa
    with pytest.raises(NoSleepDurationException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="15:00",
            fell_asleep="17:00",
            woke_up="01:00",
            got_up="03:00",
            no_sleep="09:00",
        )


def test_no_sleep_time_cannot_be_gt_sleep_time_with_three_time_points_after_midnight():  # noqa
    with pytest.raises(NoSleepDurationException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="23:00",
            fell_asleep="01:00",
            woke_up="09:00",
            got_up="11:00",
            no_sleep="09:00",
        )
