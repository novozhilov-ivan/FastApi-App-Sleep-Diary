from uuid import uuid4

import pytest

from sqlalchemy.exc import IntegrityError

from src.gateways.postgresql.database import Database
from src.gateways.postgresql.models import ORMNote, ORMUser
from tests.conftest import (
    points_order_desc_from_went_to_bed_and_one_hour_no_sleep,
    TN,
)
from tests.integration.conftest import query_insert_note


def test_unique_bedtime_date_for_user(database: Database, orm_user: ORMUser) -> None:
    points: TN = points_order_desc_from_went_to_bed_and_one_hour_no_sleep
    bedtime_date, went_to_bed, fell_asleep, woke_up, got_up, no_sleep = points
    note_oid = uuid4()
    note = {
        "oid": str(note_oid),
        "bedtime_date": bedtime_date.isoformat(),
        "owner_oid": str(orm_user.oid),
        "went_to_bed": went_to_bed.isoformat(),
        "fell_asleep": fell_asleep.isoformat(),
        "woke_up": woke_up.isoformat(),
        "got_up": got_up.isoformat(),
        "no_sleep": no_sleep.isoformat(),
    }

    with database.get_session() as session:
        session.execute(query_insert_note, note)
        db_notes: list[ORMNote] = session.query(ORMNote).all()

    assert len(db_notes) == 1
    [db_note] = db_notes

    assert isinstance(db_note, ORMNote)
    assert db_note.bedtime_date == bedtime_date

    note["oid"] = str(uuid4())

    with pytest.raises(IntegrityError):
        with database.get_session() as session:
            session.execute(query_insert_note, note)
            db_notes = session.query(ORMNote).all()

    assert len(db_notes) == 1
    [expected_first_note] = db_notes
    assert isinstance(expected_first_note, ORMNote)
    assert expected_first_note.oid == db_note.oid
