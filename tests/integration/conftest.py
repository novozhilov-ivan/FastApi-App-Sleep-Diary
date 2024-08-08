from typing import Generator

import pytest

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.orm.base import metadata


@pytest.fixture
def in_memory_db() -> Engine:
    engine = create_engine("sqlite:///:memory:")
    engine.echo = True
    metadata.create_all(engine)
    return engine


@pytest.fixture
def memory_session(in_memory_db: Engine) -> Generator[Session, None, None]:
    mem_session = sessionmaker(bind=in_memory_db)
    with mem_session() as session:
        yield session
