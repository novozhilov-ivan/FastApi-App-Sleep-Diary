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
    week.BaseWeek(notes)


def test_adding_one_note_twice_to_week() -> None:
    test_note = note.NoteValueObject(
        bedtime_date="2024-01-01",
        **times,
    )
    test_week = week.BaseWeek()
    assert len(test_week) == 0
    test_week.add(test_note)
    assert len(test_week) == 1
    test_week.add(test_note)
    assert len(test_week) == 1
