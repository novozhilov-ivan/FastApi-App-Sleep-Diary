import pytest

from src.domain import note as nt
from tests.unit.write_notes_test.sequences_test.fell_asleep_test import (
    incorrect_time_points_sequence_message,
)


def test_woke_up_cannot_be_gt_got_up() -> None:
    with pytest.raises(nt.TimePointsSequenceError) as error:
        nt.TimePointsSequencesValidator(
            bedtime_date="2020-12-12",
            went_to_bed="01:00",
            fell_asleep="03:00",
            woke_up="14:00",
            got_up="13:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_woke_up_cannot_be_gt_got_up_with_one_time_point_after_midnight_1() -> None:
    with pytest.raises(nt.TimePointsSequenceError) as error:
        nt.TimePointsSequencesValidator(
            bedtime_date="2020-12-12",
            went_to_bed="23:00",
            fell_asleep="01:00",
            woke_up="12:00",
            got_up="11:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_woke_up_cannot_be_gt_got_up_with_one_time_point_after_midnight_2() -> None:
    with pytest.raises(nt.TimePointsSequenceError) as error:
        nt.TimePointsSequencesValidator(
            bedtime_date="2020-12-12",
            went_to_bed="13:00",
            fell_asleep="15:00",
            woke_up="02:00",
            got_up="01:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_woke_up_cannot_be_gt_got_up_with_two_time_point_after_midnight_1() -> None:
    with pytest.raises(nt.TimePointsSequenceError) as error:
        nt.TimePointsSequencesValidator(
            bedtime_date="2020-12-12",
            went_to_bed="21:00",
            fell_asleep="23:00",
            woke_up="11:00",
            got_up="09:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_woke_up_cannot_be_gt_got_up_with_two_time_point_after_midnight_2() -> None:
    with pytest.raises(nt.TimePointsSequenceError) as error:
        nt.TimePointsSequencesValidator(
            bedtime_date="2020-12-12",
            went_to_bed="15:00",
            fell_asleep="17:00",
            woke_up="04:00",
            got_up="03:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message
