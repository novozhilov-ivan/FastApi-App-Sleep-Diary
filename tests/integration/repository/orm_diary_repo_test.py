from datetime import date, datetime, time
from uuid import UUID

from sqlalchemy import text

from src.domain.diary import Diary
from src.domain.note import NoteEntity, NoteTimePoints, NoteValueObject
from src.infrastructure.database import Database
from src.infrastructure.orm import ORMNote, ORMUser
from src.infrastructure.repository import BaseDiaryRepository, ORMDiaryRepository


def test_repo_can_add_and_save_note(memory_database: Database, user: ORMUser):
    note_time_points = NoteTimePoints(
        bedtime_date="2020-12-12",
        went_to_bed="13:00",
        fell_asleep="15:00",
        woke_up="23:00",
        got_up="01:00",
    )
    repository: BaseDiaryRepository = ORMDiaryRepository(memory_database)
    repository.add(note_time_points, user.oid)

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
        owner_oid=user.oid,
    )
    with memory_database.get_session() as session:
        session.add(note_orm)
        session.commit()
        session.refresh(note_orm)
    return note_orm


def test_repo_can_retrieve_note_entity_by_oid(
    memory_database: Database,
    user: ORMUser,
):
    inserted_note_orm = insert_note(memory_database, user)

    repository: BaseDiaryRepository = ORMDiaryRepository(memory_database)
    retrieved_entity: NoteEntity | None = repository.get(inserted_note_orm.oid)

    assert retrieved_entity
    assert isinstance(retrieved_entity, NoteEntity)
    assert isinstance(retrieved_entity.oid, UUID)
    assert isinstance(retrieved_entity.created_at, datetime)
    assert isinstance(retrieved_entity.updated_at, datetime)
    assert retrieved_entity.bedtime_date == date(2020, 12, 12)
    assert retrieved_entity.went_to_bed == time(13, 0)
    assert retrieved_entity.fell_asleep == time(15, 0)
    assert retrieved_entity.woke_up == time(23, 0)
    assert retrieved_entity.got_up == time(1, 0)
    assert retrieved_entity.no_sleep == time(0, 0)


def test_repo_can_retrieve_note_entity_by_bedtime_date(
    memory_database: Database,
    user: ORMUser,
):
    insert_note(memory_database, user)

    repository: BaseDiaryRepository = ORMDiaryRepository(memory_database)
    retrieved_entity: NoteEntity | None = repository.get_by_bedtime_date(
        "2020-12-12",
        user.oid,
    )

    assert retrieved_entity
    assert isinstance(retrieved_entity, NoteEntity)
    assert isinstance(retrieved_entity.oid, UUID)
    assert isinstance(retrieved_entity.created_at, datetime)
    assert isinstance(retrieved_entity.updated_at, datetime)
    assert retrieved_entity.bedtime_date == date(2020, 12, 12)
    assert retrieved_entity.went_to_bed == time(13, 0)
    assert retrieved_entity.fell_asleep == time(15, 0)
    assert retrieved_entity.woke_up == time(23, 0)
    assert retrieved_entity.got_up == time(1, 0)
    assert retrieved_entity.no_sleep == time(0, 0)


def test_repo_can_retrieve_diary(
    memory_database: Database,
    user: ORMUser,
):
    insert_note(memory_database, user)

    repository: BaseDiaryRepository = ORMDiaryRepository(memory_database)
    retrieved_diary = repository.get_diary(user.oid)
    assert isinstance(retrieved_diary, Diary)
    assert len(retrieved_diary.notes_list) == 1
    assert retrieved_diary.notes_list == {
        NoteValueObject(
            bedtime_date="2020-12-12",
            went_to_bed="13:00",
            fell_asleep="15:00",
            woke_up="23:00",
            got_up="01:00",
            no_sleep="00:00",
        ),
    }
