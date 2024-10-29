from uuid import uuid4

from src.domain.entities import NoteEntity
from src.domain.services import DiaryService
from src.domain.values.points import Points
from tests.use_cases import (
    date_point,
    points_order_desc_from_got_up,
    points_order_desc_from_went_to_bed,
)


owner_oid = uuid4()
points = Points(*points_order_desc_from_went_to_bed)
note = NoteEntity(owner_oid=owner_oid, points=points)


def test_write_one_note():
    diary = DiaryService()
    diary.write(note)
    expected_note, *_ = diary.notes_list
    assert expected_note == note


def test_write_is_idempotent() -> None:
    diary = DiaryService()
    diary.write(note)
    diary.write(note)
    assert len(diary.notes_list) == 1
    expected_note, *_ = diary.notes_list
    assert expected_note == note


def test_write_is_idempotent_by_bedtime_date_only() -> None:
    diary = DiaryService()
    diary.write(note)

    _, *other_time_points = points_order_desc_from_got_up
    note_2 = NoteEntity(
        owner_oid=owner_oid,
        points=Points(date_point, *other_time_points),
    )
    diary.write(note_2)

    assert len(diary.notes_list) == 1
    expected_note: NoteEntity
    expected_note, *_ = diary.notes_list
    assert expected_note == note
    assert expected_note.points.went_to_bed == note.points.went_to_bed
    assert expected_note.points.fell_asleep == note.points.fell_asleep
    assert expected_note.points.woke_up == note.points.woke_up
    assert expected_note.points.got_up == note.points.got_up


def test_can_write_note_in_empty_diary() -> None:
    assert DiaryService().can_write(note)


def test_cannot_write_written_note_in_diary() -> None:
    diary = DiaryService()
    diary.write(note)
    assert not diary.can_write(note)


def test_cannot_write_note_in_diary_with_same_bedtime_date() -> None:
    diary = DiaryService()
    diary.write(note)
    _, *other_time_points = points_order_desc_from_got_up
    note_2 = note
    note_2.points = Points(date_point, *other_time_points)
    assert not diary.can_write(note_2)
