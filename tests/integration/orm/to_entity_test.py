from uuid import uuid4

from src.domain.entities.note import NoteEntity
from src.domain.values.points import Points
from src.infra.database import Database
from src.infra.orm import ORMNote, ORMUser
from tests.integration.conftest import stmt_insert_note
from tests.use_cases import (
    TN,
    points_order_desc_from_went_to_bed_and_one_hour_no_sleep,
)


def test_note_orm_to_entity(memory_database: Database, user: ORMUser):
    points: TN = points_order_desc_from_went_to_bed_and_one_hour_no_sleep
    bedtime_date, went_to_bed, fell_asleep, woke_up, got_up, no_sleep = points
    note_oid = uuid4()
    note = {
        "oid": str(note_oid),
        "bedtime_date": bedtime_date.isoformat(),
        "owner_oid": str(user.oid),
        "went_to_bed": went_to_bed.isoformat(),
        "fell_asleep": fell_asleep.isoformat(),
        "woke_up": woke_up.isoformat(),
        "got_up": got_up.isoformat(),
        "no_sleep": no_sleep.isoformat(),
    }

    with memory_database.get_session() as session:
        session.execute(stmt_insert_note, note)

    db_note: ORMNote | None = session.query(ORMNote).first()
    assert isinstance(db_note, ORMNote)
    db_note_entity = db_note.to_entity()
    assert isinstance(db_note_entity, NoteEntity)

    expected_note = NoteEntity(
        oid=note_oid,
        owner_oid=user.oid,
        points=Points(
            bedtime_date=bedtime_date,
            went_to_bed=went_to_bed,
            fell_asleep=fell_asleep,
            woke_up=woke_up,
            got_up=got_up,
            no_sleep=no_sleep,
        ),
    )
    assert expected_note == db_note_entity
    assert expected_note.points.bedtime_date == db_note_entity.points.bedtime_date
    assert expected_note.points.went_to_bed == db_note_entity.points.went_to_bed
    assert expected_note.points.fell_asleep == db_note_entity.points.fell_asleep
    assert expected_note.points.woke_up == db_note_entity.points.woke_up
    assert expected_note.points.got_up == db_note_entity.points.got_up
    assert expected_note.points.no_sleep == db_note_entity.points.no_sleep
