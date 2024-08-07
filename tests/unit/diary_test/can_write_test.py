from src.domain import diary as dr, note as nt


note = nt.NoteValueObject(
    bedtime_date="2024-01-01",
    went_to_bed="01:00",
    fell_asleep="03:00",
    woke_up="11:00",
    got_up="13:00",
)


def test_can_write_note_in_empty_diary() -> None:
    assert dr.Diary().can_write(note)


def test_cannot_write_written_note_in_diary() -> None:
    diary = dr.Diary()
    diary.write(note)
    assert not diary.can_write(note)


def test_cannot_write_note_in_diary_with_same_bedtime_date() -> None:
    diary = dr.Diary()
    diary.write(note)
    note_2 = nt.NoteValueObject(
        bedtime_date="2024-01-01",
        went_to_bed="11:00",
        fell_asleep="13:00",
        woke_up="21:00",
        got_up="23:00",
    )
    assert not diary.can_write(note_2)
