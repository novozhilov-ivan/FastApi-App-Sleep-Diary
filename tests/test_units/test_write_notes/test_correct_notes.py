from src.domain.note.value_object import NoteValueObject


def test_create_note_with_increasing_sequenced_of_all_time_points():
    NoteValueObject(
        bedtime_date="2020-12-12",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
    )


def test_create_note_with_one_time_point_after_midnight():
    NoteValueObject(
        bedtime_date="2020-12-12",
        went_to_bed="13:00",
        fell_asleep="15:00",
        woke_up="23:00",
        got_up="01:00",
    )


def test_create_note_with_two_time_point_after_midnight():
    NoteValueObject(
        bedtime_date="2020-12-12",
        went_to_bed="15:00",
        fell_asleep="17:00",
        woke_up="01:00",
        got_up="03:00",
    )


def test_create_note_with_three_time_point_after_midnight():
    NoteValueObject(
        bedtime_date="2020-12-12",
        went_to_bed="23:00",
        fell_asleep="01:00",
        woke_up="09:00",
        got_up="11:00",
    )
