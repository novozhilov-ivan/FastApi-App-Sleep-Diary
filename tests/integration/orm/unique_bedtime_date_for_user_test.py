from uuid import uuid4

import pytest

from sqlalchemy.exc import IntegrityError

from src.infra.database import Database
from src.infra.orm import ORMNote, ORMUser
from tests.integration.conftest import stmt_insert_note
from tests.use_cases import (
    TN,
    points_order_desc_from_went_to_bed_and_one_hour_no_sleep,
)


def test_unique_bedtime_date_for_user(memory_database: Database, user: ORMUser):
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
        db_notes: list[ORMNote] = session.query(ORMNote).all()

    assert len(db_notes) == 1
    [db_note] = db_notes

    assert isinstance(db_note, ORMNote)
    assert db_note.bedtime_date == bedtime_date

    note["oid"] = str(uuid4())

    with memory_database.get_session() as session:
        with pytest.raises(
            expected_exception=IntegrityError,
            match="UNIQUE constraint failed: notes.bedtime_date, notes.owner_oid",
        ):
            session.execute(stmt_insert_note, note)
        db_notes = session.query(ORMNote).all()

    assert len(db_notes) == 1
    [expected_first_note] = db_notes
    assert isinstance(expected_first_note, ORMNote)
    assert expected_first_note.oid == db_note.oid
