import pytest

from src.domain.exceptions import TimePointsSequenceException
from src.domain.note import NoteTimePoints


def test_fell_asleep_cannot_be_gt_woke_up():
    with pytest.raises(TimePointsSequenceException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="01:00",
            fell_asleep="12:00",
            woke_up="11:00",
            got_up="13:00",
        )


def test_fell_asleep_cannot_be_gt_got_up():
    with pytest.raises(TimePointsSequenceException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="01:00",
            fell_asleep="14:00",
            woke_up="11:00",
            got_up="13:00",
        )


def test_fell_asleep_cannot_be_gt_woke_up_with_one_time_points_after_midnight():
    with pytest.raises(TimePointsSequenceException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="23:00",
            fell_asleep="10:00",
            woke_up="09:00",
            got_up="11:00",
        )


def test_fell_asleep_cannot_be_gt_woke_up_and_gt_got_up_with_two_time_points_after_midnight():  # noqa
    with pytest.raises(TimePointsSequenceException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="23:00",
            fell_asleep="12:00",
            woke_up="09:00",
            got_up="11:00",
        )
