from src.domain import diary as dr, note as nt


note = nt.NoteValueObject(
    bedtime_date="2024-01-01",
    went_to_bed="01:00",
    fell_asleep="03:00",
    woke_up="11:00",
    got_up="13:00",
)


def test_write_one_note() -> None:
    diary = dr.Diary()
    diary.write(note)
    expected_note, *_ = diary.notes_list
    assert expected_note == note


def test_write_is_idempotent() -> None:
    diary = dr.Diary()
    diary.write(note)
    diary.write(note)
    assert len(diary.notes_list) == 1
    expected_note, *_ = diary.notes_list
    assert expected_note == note


def test_write_is_idempotent_by_bedtime_date_only() -> None:
    diary = dr.Diary()
    diary.write(note)
    note_2 = nt.NoteValueObject(
        bedtime_date=note.bedtime_date,
        went_to_bed="02:00",
        fell_asleep="04:00",
        woke_up="12:00",
        got_up="15:00",
    )
    diary.write(note_2)
    assert len(diary.notes_list) == 1
    expected_note, *_ = diary.notes_list
    assert expected_note == note
    assert expected_note.went_to_bed == note.went_to_bed
    assert expected_note.fell_asleep == note.fell_asleep
    assert expected_note.woke_up == note.woke_up
    assert expected_note.got_up == note.got_up
