import pytest

from src.domain.note.error import TimePointsSequenceError
from src.domain.note.validators import NoteFieldsValidators
from tests.test_units.test_write_notes.test_sequences.test_fell_asleep import (
    incorrect_time_points_sequence_message,
)


def test_went_to_bed_cannot_be_gt_fell_asleep_and_lt_other_time_points() -> None:
    with pytest.raises(TimePointsSequenceError) as error:
        NoteFieldsValidators(
            bedtime_date="2020-12-12",
            went_to_bed="04:00",
            fell_asleep="03:00",
            woke_up="12:00",
            got_up="14:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_went_to_bed_cannot_be_gt_fell_asleep_with_points_after_midnight() -> None:
    with pytest.raises(TimePointsSequenceError) as error:
        NoteFieldsValidators(
            bedtime_date="2020-12-12",
            went_to_bed="14:00",
            fell_asleep="13:00",
            woke_up="02:00",
            got_up="04:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_went_to_bed_cannot_be_gt_fell_asleep_and_woke_up() -> None:
    with pytest.raises(TimePointsSequenceError) as error:
        NoteFieldsValidators(
            bedtime_date="2020-12-12",
            went_to_bed="12:00",
            fell_asleep="03:00",
            woke_up="11:00",
            got_up="13:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_went_to_bed_cannot_be_gt_woke_up_and_lt_others_points_with_some_points_after_midnight() -> (  # noqa
    None
):
    with pytest.raises(TimePointsSequenceError) as error:
        NoteFieldsValidators(
            bedtime_date="2020-12-12",
            went_to_bed="08:00",
            fell_asleep="23:00",
            woke_up="07:00",
            got_up="09:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message
