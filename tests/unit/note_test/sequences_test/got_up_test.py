import pytest

from src.domain import note as nt
from tests.unit.note_test.sequences_test.fell_asleep_test import (
    incorrect_time_points_sequence_message,
)


def test_got_up_cannot_be_lt_only_woke_up() -> None:
    with pytest.raises(nt.TimePointsSequenceError) as error:
        nt.NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="01:00",
            fell_asleep="03:00",
            woke_up="11:00",
            got_up="10:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_got_up_cannot_be_lt_only_woke_up_with_some_time_points_after_midnight() -> (
    None
):
    with pytest.raises(nt.TimePointsSequenceError) as error:
        nt.NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="23:00",
            fell_asleep="01:00",
            woke_up="07:00",
            got_up="06:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_got_up_cannot_be_gt_woke_up_and_lt_other_points_with_some_time_points_after_midnight() -> (  # noqa
    None
):
    with pytest.raises(nt.TimePointsSequenceError) as error:
        nt.NoteTimePoints(
            bedtime_date="2020-12-12",
            went_to_bed="15:00",
            fell_asleep="17:00",
            woke_up="02:00",
            got_up="01:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message
