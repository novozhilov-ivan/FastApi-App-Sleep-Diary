from typing import Generator

import pytest

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from src.orm import UserORM, metadata


insert_note_stmt = text(
    "INSERT INTO notes (oid, bedtime_date, went_to_bed, fell_asleep, "
    "woke_up, got_up, no_sleep, owner_id) "
    "VALUES (:oid, :bedtime_date, :went_to_bed, :fell_asleep, :woke_up,"
    ":got_up, :no_sleep, :owner_id);",
)


@pytest.fixture
def in_memory_db() -> Engine:
    engine = create_engine("sqlite://")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db: Engine) -> Generator[Session, None, None]:
    with sessionmaker(bind=in_memory_db)() as session:
        yield session


@pytest.fixture
def create_user(session: Session) -> UserORM:
    user = UserORM(
        username="test_user",
        password=b"test_password",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
