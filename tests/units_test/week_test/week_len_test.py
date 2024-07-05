import pytest

from pydantic import ValidationError

from src.domain import note, week


times = {
    "went_to_bed": "01:00",
    "fell_asleep": "03:00",
    "woke_up": "11:00",
    "got_up": "13:00",
}


def test_create_correct_week() -> None:
    notes = (
        note.NoteValueObject(
            bedtime_date=f"2024-01-0{day_number}",
            **times,
        )
        for day_number in range(1, 8)
    )
    week.BaseWeek(notes=set(notes))


def test_create_empty_week() -> None:
    with pytest.raises(ValidationError):
        week.BaseWeek(notes=set())


def test_create_week_with_len_gt_7() -> None:
    notes = (
        note.NoteValueObject(
            bedtime_date=f"2024-01-0{day_number}",
            **times,
        )
        for day_number in range(1, 9)
    )

    with pytest.raises(ValidationError):
        week.BaseWeek(notes=set(notes))
