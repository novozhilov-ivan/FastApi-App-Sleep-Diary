import datetime as dt

from src.domain import note as nt, week as wk


note_1 = nt.NoteValueObject(
    bedtime_date="2024-01-01",
    went_to_bed="01:00",
    fell_asleep="03:00",
    woke_up="11:00",
    got_up="13:00",
    no_sleep="00:30",
)
note_2 = nt.NoteValueObject(
    bedtime_date="2024-01-02",
    went_to_bed="01:00",
    fell_asleep="03:00",
    woke_up="12:00",
    got_up="14:00",
    no_sleep="01:00",
)


def test_average_weekly_sleep_duration_of_one_note_in_week() -> None:
    week = wk.Week({note_1})
    assert week._duration_of_week == 1
    assert week._average_weekly_sleep_duration == dt.timedelta(seconds=8 * 60 * 60)
    assert week._average_weekly_in_bed_duration == dt.timedelta(seconds=12 * 60 * 60)
    assert week._average_weekly_no_sleep_duration == dt.timedelta(seconds=30 * 60)
    assert week._average_weekly_sleep_duration_minus_no_sleep == dt.timedelta(
        seconds=8 * 60 * 60 - 30 * 60,
    )


def test_average_weekly_sleep_duration() -> None:
    week = wk.Week({note_1, note_2})
    assert week._duration_of_week == 2
    assert week._average_weekly_sleep_duration == dt.timedelta(
        seconds=(8 * 60 * 60 + 9 * 60 * 60) / 2,
    )
    assert week._average_weekly_in_bed_duration == dt.timedelta(
        seconds=(12 * 60 * 60 + 13 * 60 * 60) / 2,
    )
    assert week._average_weekly_no_sleep_duration == dt.timedelta(
        seconds=(30 * 60 + 60 * 60) / 2,
    )
    assert week._average_weekly_sleep_duration_minus_no_sleep == dt.timedelta(
        seconds=(8 * 60 * 60 + 9 * 60 * 60) / 2 - (30 * 60 + 60 * 60) / 2,
    )
