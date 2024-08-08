import pytest

from src.domain.diary import Diary
from src.domain.errors import NoteAlreadyExist
from src.domain.note import NoteStatistic, NoteValueObject
from src.domain.write import write


def test_write_one_note_in_diary() -> None:
    diary = Diary()
    note = NoteValueObject(
        bedtime_date="2024-01-01",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
    )
    written_note_entity = write(note, diary)
    assert isinstance(written_note_entity, NoteStatistic)
    assert written_note_entity.bedtime_date == note.bedtime_date
    assert written_note_entity.went_to_bed == note.went_to_bed
    assert written_note_entity.fell_asleep == note.fell_asleep
    assert written_note_entity.woke_up == note.woke_up
    assert written_note_entity.got_up == note.got_up


def test_write_note_in_diary_twice() -> None:
    diary = Diary()
    note = NoteValueObject(
        bedtime_date="2024-01-01",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
    )
    write(note, diary)

    with pytest.raises(
        expected_exception=NoteAlreadyExist,
        match=f"Запись о сне с датой {note.bedtime_date} "
        f"уже существует в дневнике.",
    ):
        write(note, diary)


def test_write_different_note_in_diary() -> None:
    diary = Diary()
    note_1 = NoteValueObject(
        bedtime_date="2024-01-01",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
    )
    note_2 = NoteValueObject(
        bedtime_date="2024-01-02",
        went_to_bed="03:00",
        fell_asleep="05:00",
        woke_up="13:00",
        got_up="15:00",
    )
    written_note_entity_1 = write(note_1, diary)
    written_note_entity_2 = write(note_2, diary)

    assert len(diary.notes_list) == 2
    note_in_diary_1, note_in_diary_2, *_ = sorted(diary.notes_list)
    assert note_in_diary_1 == written_note_entity_1
    assert note_in_diary_2 == written_note_entity_2
    assert isinstance(written_note_entity_1, NoteStatistic)
    assert isinstance(written_note_entity_2, NoteStatistic)
    assert written_note_entity_1.bedtime_date == note_1.bedtime_date
    assert written_note_entity_1.went_to_bed == note_1.went_to_bed
    assert written_note_entity_1.fell_asleep == note_1.fell_asleep
    assert written_note_entity_1.woke_up == note_1.woke_up
    assert written_note_entity_1.got_up == note_1.got_up
    assert written_note_entity_2.bedtime_date == note_2.bedtime_date
    assert written_note_entity_2.went_to_bed == note_2.went_to_bed
    assert written_note_entity_2.fell_asleep == note_2.fell_asleep
    assert written_note_entity_2.woke_up == note_2.woke_up
    assert written_note_entity_2.got_up == note_2.got_up
