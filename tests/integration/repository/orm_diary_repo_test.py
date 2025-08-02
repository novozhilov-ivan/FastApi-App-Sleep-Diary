from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import text

from src.domain.sleep_diary.entities.note import NoteEntity
from src.domain.sleep_diary.services.diary import DiaryService
from src.domain.sleep_diary.values.points import Points
from src.gateways.postresql.database import Database
from src.gateways.postresql.models import ORMNote, ORMUser
from src.infra.sleep_diary.repository.orm_notes import ORMNotesRepository
from tests.conftest import points_order_desc_from_went_to_bed


def test_repo_can_add_and_save_note(database: Database, orm_user: ORMUser) -> None:
    points = Points(*points_order_desc_from_went_to_bed)
    note_oid = uuid4()
    note = NoteEntity(
        oid=note_oid,
        owner_oid=orm_user.oid,
        points=points,
    )

    repository = ORMNotesRepository(database)
    repository.add(note)

    stmt = text(
        "SELECT bedtime_date, went_to_bed, fell_asleep, woke_up, got_up "
        "FROM notes;"
    )
    with database.get_session() as session:
        [result] = session.execute(stmt)

    assert result == (
        points.bedtime_date,
        points.went_to_bed,
        points.fell_asleep,
        points.woke_up,
        points.got_up,
    )


def insert_note(database: Database, orm_user: ORMUser, points: Points) -> ORMNote:
    note = NoteEntity(
        oid=uuid4(),
        owner_oid=orm_user.oid,
        points=points,
    )

    note_orm = ORMNote.from_entity(note)

    with database.get_session() as session:
        session.add(note_orm)
        session.commit()
        session.refresh(note_orm)
    return note_orm


def test_repo_can_retrieve_note_entity_by_oid(
    database: Database,
    orm_user: ORMUser,
) -> None:
    points = Points(*points_order_desc_from_went_to_bed)
    inserted_note_orm = insert_note(database, orm_user, points)

    repository = ORMNotesRepository(database)
    retrieved_entity: NoteEntity | None = repository.get_by_oid(
        inserted_note_orm.oid,
    )

    assert retrieved_entity
    assert isinstance(retrieved_entity, NoteEntity)
    assert isinstance(retrieved_entity.oid, UUID)
    assert isinstance(retrieved_entity.created_at, datetime)
    assert isinstance(retrieved_entity.updated_at, datetime)
    assert retrieved_entity.points.bedtime_date == points.bedtime_date
    assert retrieved_entity.points.went_to_bed == points.went_to_bed
    assert retrieved_entity.points.fell_asleep == points.fell_asleep
    assert retrieved_entity.points.woke_up == points.woke_up
    assert retrieved_entity.points.got_up == points.got_up
    assert retrieved_entity.points.no_sleep == points.no_sleep


def test_repo_can_retrieve_note_entity_by_bedtime_date(
    database: Database,
    orm_user: ORMUser,
) -> None:
    points = Points(*points_order_desc_from_went_to_bed)
    insert_note(database, orm_user, points)

    repository = ORMNotesRepository(database)
    retrieved_entity: NoteEntity | None = repository.get_by_bedtime_date(
        points.bedtime_date,
        orm_user.oid,
    )

    assert retrieved_entity
    assert isinstance(retrieved_entity, NoteEntity)
    assert isinstance(retrieved_entity.oid, UUID)
    assert isinstance(retrieved_entity.created_at, datetime)
    assert isinstance(retrieved_entity.updated_at, datetime)
    assert retrieved_entity.points.bedtime_date == points.bedtime_date
    assert retrieved_entity.points.went_to_bed == points.went_to_bed
    assert retrieved_entity.points.fell_asleep == points.fell_asleep
    assert retrieved_entity.points.woke_up == points.woke_up
    assert retrieved_entity.points.got_up == points.got_up
    assert retrieved_entity.points.no_sleep == points.no_sleep


def test_repo_can_retrieve_diary(database: Database, orm_user: ORMUser) -> None:
    points = Points(*points_order_desc_from_went_to_bed)
    insert_note(database, orm_user, points)

    repository = ORMNotesRepository(database)
    retrieved_notes = repository.get_all_notes(orm_user.oid)
    diary = DiaryService.create(retrieved_notes)

    assert isinstance(diary.notes_list, set)
    assert len(diary.notes_list) == 1

    fake_oid = uuid4()
    assert diary.notes_list == {
        NoteEntity(oid=fake_oid, owner_oid=orm_user.oid, points=points),
    }
