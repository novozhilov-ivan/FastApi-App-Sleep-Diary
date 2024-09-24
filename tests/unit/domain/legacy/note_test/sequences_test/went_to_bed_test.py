import pytest

from src.domain.exceptions import TimePointsSequenceException
from src.domain.note import NoteTimePoints


def test_went_to_bed_cannot_be_gt_fell_asleep_and_lt_other_time_points():
    with pytest.raises(TimePointsSequenceException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="04:00",
            fell_asleep="03:00",
            woke_up="12:00",
            got_up="14:00",
        )


def test_went_to_bed_cannot_be_gt_fell_asleep_with_points_after_midnight():
    with pytest.raises(TimePointsSequenceException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="14:00",
            fell_asleep="13:00",
            woke_up="02:00",
            got_up="04:00",
        )


def test_went_to_bed_cannot_be_gt_fell_asleep_and_woke_up():
    with pytest.raises(TimePointsSequenceException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="12:00",
            fell_asleep="03:00",
            woke_up="11:00",
            got_up="13:00",
        )


def test_went_to_bed_cannot_be_gt_woke_up_and_lt_others_points_with_some_points_after_midnight():  # noqa
    with pytest.raises(TimePointsSequenceException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="08:00",
            fell_asleep="23:00",
            woke_up="07:00",
            got_up="09:00",
        )
