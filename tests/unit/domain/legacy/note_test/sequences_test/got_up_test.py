import pytest

from src.domain.exceptions import TimePointsSequenceException
from src.domain.note import NoteTimePoints


def test_got_up_cannot_be_lt_only_woke_up():
    with pytest.raises(TimePointsSequenceException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="01:00",
            fell_asleep="03:00",
            woke_up="11:00",
            got_up="10:00",
        )


def test_got_up_cannot_be_lt_only_woke_up_with_some_time_points_after_midnight():
    with pytest.raises(TimePointsSequenceException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="23:00",
            fell_asleep="01:00",
            woke_up="07:00",
            got_up="06:00",
        )


def test_got_up_cannot_be_gt_woke_up_and_lt_other_points_with_some_time_points_after_midnight():  # noqa
    with pytest.raises(TimePointsSequenceException):
        NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="15:00",
            fell_asleep="17:00",
            woke_up="02:00",
            got_up="01:00",
        )
