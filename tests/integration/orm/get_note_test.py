from datetime import UTC, date, datetime, time
from uuid import uuid4

from sqlalchemy.orm import Session

from src.orm.note import NoteORM
from src.orm.user import UserORM
from tests.integration.conftest import insert_note_stmt


def test_get_note(
    memory_session: Session,
    create_user: UserORM,
) -> None:
    expected_created_at = expected_updated_at = datetime.now(
        tz=UTC,
    ).replace(
        microsecond=0,
        tzinfo=None,
    )
    expected_note_oid = uuid4()
    memory_session.execute(
        statement=insert_note_stmt,
        params=(
            {
                "oid": f"{expected_note_oid}",
                "bedtime_date": "2020-01-01",
                "went_to_bed": "01-00",
                "fell_asleep": "03-00",
                "woke_up": "11-00",
                "got_up": "13-00",
                "no_sleep": "01-00",
                "owner_id": f"{create_user.oid}",
            },
            {
                "oid": f"{uuid4()}",
                "bedtime_date": "2020-01-02",
                "went_to_bed": "02-00",
                "fell_asleep": "04-00",
                "woke_up": "12-00",
                "got_up": "14-00",
                "no_sleep": "01-10",
                "owner_id": f"{create_user.oid}",
            },
            {
                "oid": f"{uuid4()}",
                "bedtime_date": "2020-01-03",
                "went_to_bed": "03-00",
                "fell_asleep": "05-00",
                "woke_up": "13-00",
                "got_up": "15-00",
                "no_sleep": "01-20",
                "owner_id": f"{create_user.oid}",
            },
        ),
    )
    db_notes: list[NoteORM] = memory_session.query(NoteORM).all()
    assert len(db_notes) == 3
    db_note, *_ = db_notes
    assert isinstance(db_note, NoteORM)
    assert db_note.oid == expected_note_oid
    assert db_note.created_at >= expected_created_at
    assert db_note.updated_at >= expected_updated_at
    assert db_note.bedtime_date == date(2020, 1, 1)
    assert db_note.went_to_bed.replace(tzinfo=None) == time(1, 0)
    assert db_note.fell_asleep.replace(tzinfo=None) == time(3, 0)
    assert db_note.woke_up.replace(tzinfo=None) == time(11, 0)
    assert db_note.got_up.replace(tzinfo=None) == time(13, 0)
    assert db_note.no_sleep.replace(tzinfo=None) == time(1, 0)
    assert db_note.owner_id == create_user.oid
