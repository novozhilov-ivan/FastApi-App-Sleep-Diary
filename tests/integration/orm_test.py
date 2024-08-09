from sqlalchemy import text
from sqlalchemy.orm import Session

from src.domain.note import NoteEntity
from src.orm.note import NoteORM


def test_mapping(memory_session: Session) -> None:
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
    db_entity = db_note.to_entity()

    expected = NoteEntity(
        oid="a4c727fb-8c2b-4fc0-81ea-9c31ed64a4ff",
        created_at=db_entity.created_at,
        updated_at=db_entity.updated_at,
        bedtime_date="2020-01-01",
        went_to_bed="01:00",
        fell_asleep="03:00",
        woke_up="11:00",
        got_up="13:00",
        no_sleep="01:00",
    )
    assert db_entity == expected
