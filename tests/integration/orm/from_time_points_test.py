from src.domain.note import NoteTimePoints
from src.infrastructure.database import Database
from src.infrastructure.orm import ORMNote
from src.infrastructure.orm.user import ORMUser


def test_note_orm_from_time_points(
    memory_database: Database,
    exist_user: ORMUser,
):
    note_time_points = NoteTimePoints(
        bedtime_date="2020-12-12",
        went_to_bed="13:00",
        fell_asleep="15:00",
        woke_up="23:00",
        got_up="01:00",
    )
    note_orm = ORMNote.from_time_points(
        obj=note_time_points,
        owner_id=exist_user.oid,
    )

    with memory_database.get_session() as session:
        session.add(note_orm)
        session.commit()
        session.refresh(note_orm)

    assert note_orm.oid
    assert note_orm.created_at
    assert note_orm.updated_at
    assert note_orm.bedtime_date == note_time_points.bedtime_date
    assert note_orm.went_to_bed == note_time_points.went_to_bed
    assert note_orm.fell_asleep == note_time_points.fell_asleep
    assert note_orm.woke_up == note_time_points.woke_up
    assert note_orm.got_up == note_time_points.got_up
