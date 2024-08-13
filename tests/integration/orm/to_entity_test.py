from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy.orm import Session

from src.domain.note import NoteEntity
from src.orm.note import NoteORM
from src.orm.user import UserORM
from tests.integration.conftest import insert_note_stmt


def test_note_orm_t_entity(
    memory_session: Session,
    create_user: UserORM,
) -> None:
    note = {
        "oid": f"{uuid4()}",
        "created_at": datetime.now(UTC).replace(microsecond=0, tzinfo=None),
        "updated_at": datetime.now(UTC).replace(microsecond=0, tzinfo=None),
        "bedtime_date": "2020-01-01",
        "went_to_bed": "01:00",
        "fell_asleep": "03:00",
        "woke_up": "11:00",
        "got_up": "13:00",
        "no_sleep": "01:00",
        "owner_id": f"{create_user.oid}",
    }
    memory_session.execute(insert_note_stmt, note)
    memory_session.commit()
    db_note: NoteORM | None = memory_session.query(NoteORM).first()
    assert isinstance(db_note, NoteORM)
    db_note_entity = db_note.to_entity()
    assert isinstance(db_note_entity, NoteEntity)

    note.pop("owner_id")
    expected_note = NoteEntity.model_validate(note)
    assert expected_note == db_note_entity
    assert expected_note.created_at == db_note_entity.created_at
    assert expected_note.updated_at == db_note_entity.updated_at
    assert expected_note.bedtime_date == db_note_entity.bedtime_date
    assert expected_note.went_to_bed == db_note_entity.went_to_bed
    assert expected_note.fell_asleep == db_note_entity.fell_asleep
    assert expected_note.woke_up == db_note_entity.woke_up
    assert expected_note.got_up == db_note_entity.got_up
    assert expected_note.no_sleep == db_note_entity.no_sleep
