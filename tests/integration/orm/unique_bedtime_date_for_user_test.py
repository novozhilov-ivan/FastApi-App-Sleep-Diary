from datetime import date
from uuid import uuid4

import pytest

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.orm.note import NoteORM
from src.orm.user import UserORM
from tests.integration.conftest import insert_note_stmt


def test_unique_bedtime_date_for_user(
    session: Session,
    create_user: UserORM,
) -> None:
    note = {
        "oid": f"{uuid4()}",
        "bedtime_date": "2020-01-01",
        "went_to_bed": "01-00",
        "fell_asleep": "03-00",
        "woke_up": "11-00",
        "got_up": "13-00",
        "no_sleep": "01-00",
        "owner_id": f"{create_user.oid}",
    }
    session.execute(insert_note_stmt, note)
    session.commit()
    db_notes: list[NoteORM] = session.query(NoteORM).all()
    assert len(db_notes) == 1
    [db_note] = db_notes
    assert isinstance(db_note, NoteORM)
    assert db_note.bedtime_date == date(2020, 1, 1)
    with pytest.raises(
        expected_exception=IntegrityError,
        match="UNIQUE constraint failed: notes.bedtime_date, notes.owner_id",
    ):
        session.execute(insert_note_stmt, note)
    db_notes = session.query(NoteORM).all()
    assert len(db_notes) == 1
