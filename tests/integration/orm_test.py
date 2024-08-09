from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain.note import NoteEntity
from src.orm.note import NoteORM


def test_transfer_from_db_table_entry_to_entity(memory_session: Session) -> None:
    memory_session.execute(
        text(
            "INSERT INTO notes (oid, bedtime_date, went_to_bed, fell_asleep, "
            "woke_up, got_up, no_sleep) "
            'VALUES ("a4c727fb-8c2b-4fc0-81ea-9c31ed64a4ff", "2020-01-01", "01-00", '
            '"03-00", "11-00", "13-00", "01-00");',
        ),
    )
    db_note: NoteORM | None = memory_session.query(NoteORM).first()
    assert isinstance(db_note, NoteORM)
    entity_from_db = db_note.to_entity()
    expected = NoteEntity(
        oid=UUID("a4c727fb-8c2b-4fc0-81ea-9c31ed64a4ff"),
        created_at=entity_from_db.created_at,
        updated_at=entity_from_db.updated_at,
        bedtime_date="2020-01-01",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
        no_sleep="01:00",
    )
    assert entity_from_db == expected
