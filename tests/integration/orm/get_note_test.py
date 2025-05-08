from uuid import uuid4

from src.infra.database import Database
from src.infra.orm import ORMNote, ORMUser
from tests.conftest import (
    points_order_desc_from_went_to_bed_and_one_hour_no_sleep,
    TN,
)
from tests.integration.conftest import stmt_insert_note


def test_get_note(memory_database: Database, user: ORMUser):
    expected_note_oid = uuid4()
    points: TN = points_order_desc_from_went_to_bed_and_one_hour_no_sleep
    bedtime_date, went_to_bed, fell_asleep, woke_up, got_up, no_sleep = points
    bedtime_date = bedtime_date.replace(month=bedtime_date.month - 2)

    with memory_database.get_session() as session:
        session.execute(
            statement=stmt_insert_note,
            params=(
                {
                    "oid": f"{expected_note_oid}",
                    "owner_oid": f"{user.oid}",
                    "bedtime_date": bedtime_date.isoformat(),
                    "went_to_bed": went_to_bed.isoformat(),
                    "fell_asleep": fell_asleep.isoformat(),
                    "woke_up": woke_up.isoformat(),
                    "got_up": got_up.isoformat(),
                    "no_sleep": no_sleep.isoformat(),
                },
                {
                    "oid": f"{uuid4()}",
                    "owner_oid": f"{user.oid}",
                    "bedtime_date": bedtime_date.replace(
                        day=bedtime_date.day + 1,
                    ).isoformat(),
                    "went_to_bed": went_to_bed.replace(
                        hour=went_to_bed.hour + 1,
                    ).isoformat(),
                    "fell_asleep": fell_asleep.replace(
                        hour=fell_asleep.hour + 1,
                    ).isoformat(),
                    "woke_up": woke_up.replace(hour=woke_up.hour + 1).isoformat(),
                    "got_up": got_up.replace(hour=got_up.hour + 1).isoformat(),
                    "no_sleep": no_sleep.replace(hour=no_sleep.hour + 1).isoformat(),
                },
                {
                    "oid": f"{uuid4()}",
                    "owner_oid": f"{user.oid}",
                    "bedtime_date": bedtime_date.replace(
                        day=bedtime_date.day + 2,
                    ).isoformat(),
                    "went_to_bed": went_to_bed.replace(
                        hour=went_to_bed.hour + 2,
                    ).isoformat(),
                    "fell_asleep": fell_asleep.replace(
                        hour=fell_asleep.hour + 2,
                    ).isoformat(),
                    "woke_up": woke_up.replace(hour=woke_up.hour + 2).isoformat(),
                    "got_up": got_up.replace(hour=got_up.hour + 2).isoformat(),
                    "no_sleep": no_sleep.replace(hour=no_sleep.hour + 2).isoformat(),
                },
            ),
        )
    db_notes: list[ORMNote] = session.query(ORMNote).all()
    assert len(db_notes) == 3
    db_note, *_ = db_notes
    assert isinstance(db_note, ORMNote)
    assert db_note.oid == expected_note_oid
    assert db_note.owner_oid == user.oid
    assert db_note.bedtime_date == bedtime_date
    assert db_note.went_to_bed.replace(tzinfo=None) == went_to_bed
    assert db_note.fell_asleep.replace(tzinfo=None) == fell_asleep
    assert db_note.woke_up.replace(tzinfo=None) == woke_up
    assert db_note.got_up.replace(tzinfo=None) == got_up
    assert db_note.no_sleep.replace(tzinfo=None) == no_sleep
