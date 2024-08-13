from typing import Generator

import pytest

from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from src.orm.base import metadata
from src.orm.user import UserORM


insert_note_stmt = text(
    "INSERT INTO notes (oid, bedtime_date, went_to_bed, fell_asleep, "
    "woke_up, got_up, no_sleep, owner_id) "
    "VALUES (:oid, :bedtime_date, :went_to_bed, :fell_asleep, :woke_up,"
    ":got_up, :no_sleep, :owner_id);",
)


@pytest.fixture
def in_memory_db() -> Engine:
    engine = create_engine("sqlite://")
    from src.orm.note import NoteORM  # noqa
    from src.orm.user import UserORM  # noqa

    metadata.create_all(engine)
    return engine


@pytest.fixture
def memory_session(in_memory_db: Engine) -> Generator[Session, None, None]:
    mem_session = sessionmaker(bind=in_memory_db)
    with mem_session() as session:
        yield session


@pytest.fixture
def create_user(memory_session: Session) -> UserORM:
    user = UserORM(
        username="test_user",
        password=b"test_password",
    )
    memory_session.add(user)
    memory_session.commit()
    memory_session.refresh(user)
    return user
