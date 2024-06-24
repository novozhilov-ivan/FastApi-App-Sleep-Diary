import pytest

from src.domain.note.model import Note
from src.domain.note.validators import ValidateSleepTimePointError


def test_went_to_bed_cannot_be_gt_fell_asleep_and_lt_other_time_points():
    with pytest.raises(ValidateSleepTimePointError) as error:
        Note(
            bedtime_date="2020-12-12",
            went_to_bed="04:00",
            fell_asleep="03:00",
            woke_up="12:00",
            got_up="14:00",
        )
    assert error.value.message == ValidateSleepTimePointError().message


def test_went_to_bed_cannot_be_gt_fell_asleep_and_woke_up_and_lt_got_up():
    with pytest.raises(ValidateSleepTimePointError) as error:
        Note(
            bedtime_date="2020-12-12",
            went_to_bed="12:00",
            fell_asleep="03:00",
            woke_up="11:00",
            got_up="13:00",
        )
    assert error.value.message == ValidateSleepTimePointError().message
