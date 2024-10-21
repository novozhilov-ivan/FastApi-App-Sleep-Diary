from datetime import date, time
from uuid import uuid4

import pytest

from src.domain.entities.note import NoteEntity
from src.domain.exceptions import NonUniqueNoteBedtimeDateException
from src.infrastructure.repository import BaseDiaryRepository
from src.service_layer import Diary
from tests.use_cases import (
    points_order_desc_from_went_to_bed,
)


@pytest.mark.parametrize(
    "no_sleep",
    [
        None,
        time(),
        time(0, 22),
    ],
)
def test_service_diary_can_write_with_different_value_in_no_sleep(
    diary: Diary,
    diary_repository: BaseDiaryRepository,
    no_sleep: time | None,
):
    fake_owner_oid = uuid4()
    points = (*points_order_desc_from_went_to_bed, no_sleep)

    diary.write(fake_owner_oid, *points)

    expected_bedtime_date, *_ = points
    retrieved = diary_repository.get_by_bedtime_date(
        expected_bedtime_date,
        fake_owner_oid,
    )
    assert retrieved is not None
    assert isinstance(retrieved, NoteEntity)


def test_write_one_note_in_diary(
    diary: Diary,
    diary_repository: BaseDiaryRepository,
):
    fake_owner_oid = uuid4()
    points = points_order_desc_from_went_to_bed
    diary.write(fake_owner_oid, *points)

    expected_bedtime_date, *_ = points_order_desc_from_went_to_bed
    written_note = diary_repository.get_by_bedtime_date(
        expected_bedtime_date,
        fake_owner_oid,
    )

    assert isinstance(written_note, NoteEntity)
    assert written_note.points.bedtime_date in points
    assert written_note.points.went_to_bed in points
    assert written_note.points.fell_asleep in points
    assert written_note.points.woke_up in points
    assert written_note.points.got_up in points


def test_write_note_in_diary_twice(diary: Diary):
    fake_owner_oid = uuid4()
    points = points_order_desc_from_went_to_bed
    diary.write(fake_owner_oid, *points)

    with pytest.raises(NonUniqueNoteBedtimeDateException):
        diary.write(fake_owner_oid, *points)


def test_write_different_note_in_diary(
    diary: Diary,
    diary_repository: BaseDiaryRepository,
):
    fake_owner_oid = uuid4()
    first_bedtime_date: date
    first_bedtime_date, *time_points = points_order_desc_from_went_to_bed
    second_bedtime_date = date(
        first_bedtime_date.year,
        first_bedtime_date.month,
        first_bedtime_date.day + 1,
    )

    points_1 = points_order_desc_from_went_to_bed
    points_2 = (second_bedtime_date, *time_points)

    diary.write(fake_owner_oid, *points_1)
    diary.write(fake_owner_oid, *points_2)

    notes = diary_repository.get_all_notes(fake_owner_oid)
    assert len(notes) == 2
    note_in_diary_1, note_in_diary_2, *_ = sorted(notes)

    assert note_in_diary_1.points.bedtime_date in points_1
    assert note_in_diary_1.points.went_to_bed in points_1
    assert note_in_diary_1.points.fell_asleep in points_1
    assert note_in_diary_1.points.woke_up in points_1
    assert note_in_diary_1.points.got_up in points_1

    assert note_in_diary_2.points.bedtime_date in points_2
    assert note_in_diary_2.points.went_to_bed in points_2
    assert note_in_diary_2.points.fell_asleep in points_2
    assert note_in_diary_2.points.woke_up in points_2
    assert note_in_diary_2.points.got_up in points_2
