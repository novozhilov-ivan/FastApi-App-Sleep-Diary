from datetime import date, datetime, time
from uuid import UUID

from sqlalchemy import text

from src.domain.diary import Diary
from src.domain.note import NoteEntity, NoteTimePoints, NoteValueObject
from src.infrastructure import repository
from src.infrastructure.database import Database
from src.infrastructure.orm import ORMNote, ORMUser


def test_repo_can_add_and_save_note(memory_database: Database, exist_user: ORMUser):
    note_time_points = NoteTimePoints(
        bedtime_date="2020-12-12",
        went_to_bed="13:00",
        fell_asleep="15:00",
        woke_up="23:00",
        got_up="01:00",
    )
    repo = repository.ORMDiaryRepository(memory_database)
    repo.add(ORMNote.from_time_points(note_time_points, exist_user.oid))

    with memory_database.get_session() as session:
        [result] = session.execute(
            text(
                "SELECT bedtime_date, went_to_bed, fell_asleep, woke_up, got_up "
                'FROM "notes";',
            ),
        )
    assert result == (
        "2020-12-12",
        "13:00:00.000000",
        "15:00:00.000000",
        "23:00:00.000000",
        "01:00:00.000000",
    )


def insert_note(memory_database: Database, user: ORMUser) -> ORMNote:
    note_time_points = NoteTimePoints(
        bedtime_date="2020-12-12",
        went_to_bed="13:00",
        fell_asleep="15:00",
        woke_up="23:00",
        got_up="01:00",
    )
    note_orm = ORMNote.from_time_points(
        obj=note_time_points,
        owner_id=user.oid,
    )
    with memory_database.get_session() as session:
        session.add(note_orm)
        session.commit()
        session.refresh(note_orm)
    return note_orm


def test_repo_can_retrieve_note_entity_by_oid(
    memory_database: Database,
    exist_user: ORMUser,
):
    inserted_note_orm = insert_note(memory_database, exist_user)

    repo = repository.ORMDiaryRepository(memory_database)
    retrieved: ORMNote | None = repo.get(inserted_note_orm.oid)

    assert retrieved
    assert isinstance(retrieved, ORMNote)
    entity = retrieved.to_entity()
    assert isinstance(entity, NoteEntity)
    assert isinstance(entity.oid, UUID)
    assert isinstance(entity.created_at, datetime)
    assert isinstance(entity.updated_at, datetime)
    assert entity.bedtime_date == date(2020, 12, 12)
    assert entity.went_to_bed == time(13, 0)
    assert entity.fell_asleep == time(15, 0)
    assert entity.woke_up == time(23, 0)
    assert entity.got_up == time(1, 0)
    assert entity.no_sleep == time(0, 0)


def test_repo_can_retrieve_note_entity_by_bedtime_date(
    memory_database: Database,
    exist_user: ORMUser,
):
    insert_note(memory_database, exist_user)

    repo = repository.ORMDiaryRepository(memory_database)
    retrieved: ORMNote | None = repo.get_by_bedtime_date(
        "2020-12-12",
        exist_user.oid,
    )

    assert retrieved
    assert isinstance(retrieved, ORMNote)
    entity = retrieved.to_entity()
    assert isinstance(entity, NoteEntity)
    assert isinstance(entity.oid, UUID)
    assert isinstance(entity.created_at, datetime)
    assert isinstance(entity.updated_at, datetime)
    assert entity.bedtime_date == date(2020, 12, 12)
    assert entity.went_to_bed == time(13, 0)
    assert entity.fell_asleep == time(15, 0)
    assert entity.woke_up == time(23, 0)
    assert entity.got_up == time(1, 0)
    assert entity.no_sleep == time(0, 0)


def test_repo_can_retrieve_diary(
    memory_database: Database,
    exist_user: ORMUser,
):
    insert_note(memory_database, exist_user)

    repo = repository.ORMDiaryRepository(memory_database)
    retrieved = repo.get_diary(exist_user.oid)
    assert isinstance(retrieved, Diary)
    assert len(retrieved.notes_list) == 1
    assert retrieved.notes_list == {
        NoteValueObject(
            bedtime_date="2020-12-12",
            went_to_bed="13:00",
            fell_asleep="15:00",
            woke_up="23:00",
            got_up="01:00",
            no_sleep="00:00",
        ),
    }
