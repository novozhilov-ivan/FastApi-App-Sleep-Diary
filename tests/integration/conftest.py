import pytest

from sqlalchemy import text

from src.infrastructure.database import Database
from src.infrastructure.orm import ORMUser, metadata


insert_note_stmt = text(
    "INSERT INTO notes (oid, bedtime_date, went_to_bed, fell_asleep, "
    "woke_up, got_up, no_sleep, owner_oid) "
    "VALUES (:oid, :bedtime_date, :went_to_bed, :fell_asleep, :woke_up,"
    ":got_up, :no_sleep, :owner_oid);",
)


@pytest.fixture
def memory_database() -> Database:
    database = Database(url="sqlite://")
    metadata.drop_all(database.engine)
    metadata.create_all(database.engine)
    return database


@pytest.fixture
def user(memory_database: Database) -> ORMUser:
    user = ORMUser(
        username="test_user",
        password=b"test_password",
    )
    with memory_database.get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user
