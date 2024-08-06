import datetime as dt

from src.domain import diary as dr, note as nt, week as wk


times = {
    "went_to_bed": "01:00",
    "fell_asleep": "03:00",
    "woke_up": "11:00",
    "got_up": "13:00",
}
meta = {
    "oid": 1,
    "created_at": dt.datetime.now(tz=dt.timezone.utc),
    "updated_at": dt.datetime.now(tz=dt.timezone.utc),
}


def test_create_diary_with_one_note() -> None:
    note = nt.NoteValueObject(
        bedtime_date="2024-01-01",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
    )
    diary = dr.Diary()
    week = wk.Week()
    week.add(note)
    diary.weeks.append(week)
    assert diary.notes_count == 1
    assert diary.weeks_count == 1


# def test_() -> None:
