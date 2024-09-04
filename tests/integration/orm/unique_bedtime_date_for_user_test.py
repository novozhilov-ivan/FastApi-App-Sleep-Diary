from datetime import date
from uuid import uuid4

import pytest

from sqlalchemy.exc import IntegrityError

from src.infrastructure.database import Database
from src.infrastructure.orm import ORMNote
from src.infrastructure.orm.user import ORMUser
from tests.integration.conftest import insert_note_stmt


def test_unique_bedtime_date_for_user(
    memory_database: Database,
    user: ORMUser,
):
    note = {
        "oid": f"{uuid4()}",
        "bedtime_date": "2020-01-01",
        "went_to_bed": "01-00",
        "fell_asleep": "03-00",
        "woke_up": "11-00",
        "got_up": "13-00",
        "no_sleep": "01-00",
        "owner_oid": f"{user.oid}",
    }

    with memory_database.get_session() as session:
        session.execute(insert_note_stmt, note)

    db_notes: list[ORMNote] = session.query(ORMNote).all()
    assert len(db_notes) == 1
    [db_note] = db_notes
    assert isinstance(db_note, ORMNote)
    assert db_note.bedtime_date == date(2020, 1, 1)
    with pytest.raises(
        expected_exception=IntegrityError,
        match="UNIQUE constraint failed: notes.bedtime_date, notes.owner_oid",
    ):
        session.execute(insert_note_stmt, note)
    db_notes = session.query(ORMNote).all()
    assert len(db_notes) == 1
