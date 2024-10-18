from uuid import uuid4

from src.domain.entities.note import NoteEntity
from src.domain.values.points import Points
from src.infrastructure.database import Database
from src.infrastructure.orm import ORMNote
from src.infrastructure.orm.user import ORMUser
from tests.use_cases import (
    points_order_desc_from_went_to_bed_and_one_hour_no_sleep,
)


def test_note_orm_from_time_points(memory_database: Database, user: ORMUser):
    note = NoteEntity(
        oid=uuid4(),
        owner_oid=user.oid,
        points=Points(*points_order_desc_from_went_to_bed_and_one_hour_no_sleep),
    )
    note_orm = ORMNote.from_entity(note)

    with memory_database.get_session() as session:
        session.add(note_orm)
        session.commit()
        session.refresh(note_orm)

    assert note_orm.oid
    assert note_orm.created_at
    assert note_orm.updated_at
    assert note_orm.owner_oid
    assert note_orm.bedtime_date == note.points.bedtime_date
    assert note_orm.went_to_bed == note.points.went_to_bed
    assert note_orm.fell_asleep == note.points.fell_asleep
    assert note_orm.woke_up == note.points.woke_up
    assert note_orm.got_up == note.points.got_up
