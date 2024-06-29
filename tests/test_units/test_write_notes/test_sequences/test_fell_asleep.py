import pytest

from src.domain.note.error import TimePointsSequenceError
from src.domain.note.validators import NoteFieldsValidators


incorrect_time_points_sequence_message = (
    "Некорректная последовательность временных точек записи."
)


def test_fell_asleep_cannot_be_gt_woke_up() -> None:
    with pytest.raises(TimePointsSequenceError) as error:
        NoteFieldsValidators(
            bedtime_date="2020-12-12",
            went_to_bed="01:00",
            fell_asleep="12:00",
            woke_up="11:00",
            got_up="13:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_fell_asleep_cannot_be_gt_got_up() -> None:
    with pytest.raises(TimePointsSequenceError) as error:
        NoteFieldsValidators(
            bedtime_date="2020-12-12",
            went_to_bed="01:00",
            fell_asleep="14:00",
            woke_up="11:00",
            got_up="13:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_fell_asleep_cannot_be_gt_woke_up_with_one_time_points_after_midnight() -> (
    None
):
    with pytest.raises(TimePointsSequenceError) as error:
        NoteFieldsValidators(
            bedtime_date="2020-12-12",
            went_to_bed="23:00",
            fell_asleep="10:00",
            woke_up="09:00",
            got_up="11:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message


def test_fell_asleep_cannot_be_gt_woke_up_and_gt_got_up_with_two_time_points_after_midnight() -> (  # noqa
    None
):
    with pytest.raises(TimePointsSequenceError) as error:
        NoteFieldsValidators(
            bedtime_date="2020-12-12",
            went_to_bed="23:00",
            fell_asleep="12:00",
            woke_up="09:00",
            got_up="11:00",
        )
    assert error.value.message == incorrect_time_points_sequence_message
