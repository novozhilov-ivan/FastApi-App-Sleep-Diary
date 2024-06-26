import pytest

from src.domain.note.value_object import NoteValueObject
from src.domain.note.validators import TimePointsSequenceError


def test_got_up_cannot_be_lt_only_woke_up():
    with pytest.raises(TimePointsSequenceError) as error:
        NoteValueObject(
            bedtime_date="2020-12-12",
            went_to_bed="01:00",
            fell_asleep="03:00",
            woke_up="11:00",
            got_up="10:00",
        )
    assert error.value.message == "При проверки поля с временем произошла ошибка."


def test_got_up_cannot_be_lt_only_woke_up_with_some_time_points_after_midnight():
    with pytest.raises(TimePointsSequenceError) as error:
        NoteValueObject(
            bedtime_date="2020-12-12",
            went_to_bed="23:00",
            fell_asleep="01:00",
            woke_up="07:00",
            got_up="06:00",
        )
    assert error.value.message == "При проверки поля с временем произошла ошибка."


def test_got_up_cannot_be_gt_woke_up_and_lt_other_points_with_some_time_points_after_midnight():
    with pytest.raises(TimePointsSequenceError) as error:
        NoteValueObject(
            bedtime_date="2020-12-12",
            went_to_bed="15:00",
            fell_asleep="17:00",
            woke_up="02:00",
            got_up="01:00",
        )
    assert error.value.message == "При проверки поля с временем произошла ошибка."
