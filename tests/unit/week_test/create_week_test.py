from src.domain import note as nt, week as wk


times = {
    "went_to_bed": "01:00",
    "fell_asleep": "03:00",
    "woke_up": "11:00",
    "got_up": "13:00",
}


def test_create_correct_week() -> None:
    notes = (
        nt.NoteValueObject(
            bedtime_date=f"2024-01-0{day_number}",
            **times,
        )
        for day_number in range(1, 8)
    )
    week = wk.BaseWeekStorage(notes)
    assert len(week) == 7


def test_adding_one_note_twice_to_week() -> None:
    test_note = nt.NoteValueObject(
        bedtime_date="2024-01-01",
        **times,
    )
    week = wk.BaseWeekStorage()
    assert len(week) == 0
    week.add(test_note)
    assert len(week) == 1
    week.add(test_note)
    assert len(week) == 1
