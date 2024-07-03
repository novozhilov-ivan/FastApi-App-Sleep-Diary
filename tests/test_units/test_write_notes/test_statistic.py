from datetime import time

from src.domain import note as nt


class NoteStatistic(
    nt.NoteDurations,
    nt.NoteStatistic,
):
    ...  # fmt: skip


def test_note_statistic_with_zero_time_points() -> None:
    note = NoteStatistic(
        bedtime_date="2020-12-12",
        went_to_bed="00:00",
        fell_asleep="00:00",
        woke_up="00:00",
        got_up="00:00",
        no_sleep="00:00",
    )
    assert note.time_in_sleep == time(hour=0)
    assert note.time_in_bed == time(hour=0)
    assert note.sleep_efficiency == round(0, 2)


def test_note_statistic_with_no_sleep_gt_sleep_duration() -> None:
    note = NoteStatistic(
        bedtime_date="2020-12-12",
        went_to_bed="00:00",
        fell_asleep="00:00",
        woke_up="00:00",
        got_up="00:00",
        no_sleep="10:00",
    )
    assert note.time_in_sleep == time(hour=0)
    assert note.time_in_bed == time(hour=0)
    assert note.sleep_efficiency == round(0, 2)


def test_note_statistic_correct_time_points() -> None:
    note = NoteStatistic(
        bedtime_date="2020-12-12",
        went_to_bed="01:25",
        fell_asleep="01:45",
        woke_up="09:53",
        got_up="10:09",
        no_sleep="00:11",
    )
    assert note.time_in_sleep == time(hour=7, minute=57)
    assert note.time_in_bed == time(hour=8, minute=44)
    assert note.sleep_efficiency == round((7 * 60 + 57) / (8 * 60 + 46), 2)


def test_note_statistic_all_time_points_after_midnight() -> None:
    note = NoteStatistic(
        bedtime_date="2020-12-12",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
        no_sleep="01:00",
    )
    assert note.time_in_sleep == time(hour=7)
    assert note.time_in_bed == time(hour=12)
    assert note.sleep_efficiency == round(7 / 12, 2)


def test_note_statistic_with_one_time_point_after_midnight() -> None:
    note = NoteStatistic(
        bedtime_date="2020-12-12",
        went_to_bed="13:00",
        fell_asleep="15:00",
        woke_up="23:00",
        got_up="01:00",
        no_sleep="01:00",
    )
    assert note.time_in_sleep == time(hour=7)
    assert note.time_in_bed == time(hour=12)
    assert note.sleep_efficiency == round(7 / 12, 2)


def test_note_statistic_with_two_time_point_after_midnight() -> None:
    note = NoteStatistic(
        bedtime_date="2020-12-12",
        went_to_bed="15:00",
        fell_asleep="17:00",
        woke_up="01:00",
        got_up="03:00",
        no_sleep="01:00",
    )
    assert note.time_in_sleep == time(hour=7)
    assert note.time_in_bed == time(hour=12)
    assert note.sleep_efficiency == round(7 / 12, 2)


def test_note_statistic_with_three_time_point_after_midnight() -> None:
    note = NoteStatistic(
        bedtime_date="2020-12-12",
        went_to_bed="23:00",
        fell_asleep="01:00",
        woke_up="09:00",
        got_up="11:00",
        no_sleep="01:00",
    )
    assert note.time_in_sleep == time(hour=7)
    assert note.time_in_bed == time(hour=12)
    assert note.sleep_efficiency == round(7 / 12, 2)
