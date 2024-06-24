import pytest

from src.domain.note.error import NoSleepTimeError
from src.domain.note.model import Note


def test_no_sleep_time_cannot_be_gt_sleep_time_with_increases_time_points():
    with pytest.raises(NoSleepTimeError) as error:
        Note(
            bedtime_date="2020-12-12",
            went_to_bed="01:00",
            fell_asleep="03:00",
            woke_up="11:00",
            got_up="13:00",
            no_sleep="09:00",
        )
    assert (
        error.value.message
        == "Время без сна должно быть меньше или равно времени сна."
    )


def test_no_sleep_time_cannot_be_gt_sleep_time_with_one_time_points_after_midnight():
    with pytest.raises(NoSleepTimeError) as error:
        Note(
            bedtime_date="2020-12-12",
            went_to_bed="13:00",
            fell_asleep="15:00",
            woke_up="23:00",
            got_up="01:00",
            no_sleep="09:00",
        )
    assert (
        error.value.message
        == "Время без сна должно быть меньше или равно времени сна."
    )


def test_no_sleep_time_cannot_be_gt_sleep_time_with_two_time_points_after_midnight():
    with pytest.raises(NoSleepTimeError) as error:
        Note(
            bedtime_date="2020-12-12",
            went_to_bed="15:00",
            fell_asleep="17:00",
            woke_up="01:00",
            got_up="03:00",
            no_sleep="09:00",
        )
    assert (
        error.value.message
        == "Время без сна должно быть меньше или равно времени сна."
    )


def test_no_sleep_time_cannot_be_gt_sleep_time_with_three_time_points_after_midnight():
    with pytest.raises(NoSleepTimeError) as error:
        Note(
            bedtime_date="2020-12-12",
            went_to_bed="23:00",
            fell_asleep="01:00",
            woke_up="09:00",
            got_up="11:00",
            no_sleep="09:00",
        )
    assert (
        error.value.message
        == "Время без сна должно быть меньше или равно времени сна."
    )
