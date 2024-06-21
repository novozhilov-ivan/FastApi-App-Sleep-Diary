from src.domain.note.model import Note


def test_create_note():
    note = Note(
        bedtime_date="2020-12-12",
        went_to_bed="00:10",
        fell_asleep="00:30",
        woke_up="08:40",
        got_up="09:00",
        no_sleep="00:10",
    )
