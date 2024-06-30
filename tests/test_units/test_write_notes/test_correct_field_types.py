from datetime import date, time

from src.domain.note import NoteValueObject


def test_field_types() -> None:
    note = NoteValueObject(
        bedtime_date="2020-12-12",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
        no_sleep="01:00",
    )
    assert isinstance(note.bedtime_date, date)
    assert isinstance(note.went_to_bed, time)
    assert isinstance(note.fell_asleep, time)
    assert isinstance(note.woke_up, time)
    assert isinstance(note.got_up, time)
    assert isinstance(note.no_sleep, time)
