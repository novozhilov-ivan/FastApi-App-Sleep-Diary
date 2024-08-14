import datetime as dt

from src.domain import note as nt


def test_field_types() -> None:
    note = nt.NoteValueObject(
        bedtime_date="2020-12-12",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
        no_sleep="01:00",
    )
    assert isinstance(note.bedtime_date, dt.date)
    assert isinstance(note.went_to_bed, dt.time)
    assert isinstance(note.fell_asleep, dt.time)
    assert isinstance(note.woke_up, dt.time)
    assert isinstance(note.got_up, dt.time)
    assert isinstance(note.no_sleep, dt.time)
