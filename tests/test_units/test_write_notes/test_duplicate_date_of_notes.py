from src.domain.note.value_object import NoteValueObject


note_1 = NoteValueObject(
    bedtime_date="2020-12-12",
    went_to_bed="01:00",
    fell_asleep="03:00",
    woke_up="11:00",
    got_up="13:00",
)
note_2 = NoteValueObject(
    bedtime_date="2020-12-12",
    went_to_bed="11:00",
    fell_asleep="13:00",
    woke_up="21:00",
    got_up="23:00",
)


def test_notes_is_equals_by_bedtime_date() -> None:
    assert note_1 == note_2


def test_cannot_add_notes_with_same_bedtime_date_in_week_gt_one_time_and_adding_is_idempotent() -> (  # noqa
    None
):
    week = set()
    week.add(note_1)
    assert note_1 in week
    week.add(note_2)
    assert len(week) == 1
    unique_note_of_week: NoteValueObject
    unique_note_of_week, *_ = week
    assert unique_note_of_week.went_to_bed == note_1.went_to_bed
    assert unique_note_of_week.fell_asleep == note_1.fell_asleep
    assert unique_note_of_week.woke_up == note_1.woke_up
    assert unique_note_of_week.got_up == note_1.got_up
