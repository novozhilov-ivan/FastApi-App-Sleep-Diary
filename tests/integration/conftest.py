from collections.abc import Generator
from typing import cast
from uuid import UUID

import pytest

from sqlalchemy import create_engine, delete, Engine, text
from sqlalchemy.orm import Session

from src.application.api.sleep_diary.services.diary import Diary
from src.domain.sleep_diary.services.base import INotesRepository
from src.gateways.postresql.database import Database
from src.gateways.postresql.models.user import ORMUser
from src.infra.sleep_diary.repository.orm_notes import ORMNotesRepository
from src.project.settings import PostgreSQLSettings


query_insert_note = text(
    "INSERT INTO notes (oid, bedtime_date, owner_oid, went_to_bed, fell_asleep, "
    "woke_up, got_up, no_sleep) "
    "VALUES (:oid, :bedtime_date, :owner_oid, "
    ":went_to_bed, :fell_asleep, :woke_up, :got_up, :no_sleep);",
)
stmt_check_database = text(
    "SELECT 1 FROM pg_database WHERE datname = :test_db_name;",
)
query_create_database = text("CREATE DATABASE :test_db_name;")


@pytest.fixture(scope="session")
def postgres_settings() -> PostgreSQLSettings:
    return PostgreSQLSettings()


@pytest.fixture(scope="session")
def engine(postgres_settings: PostgreSQLSettings) -> Engine:
    test_db_name = postgres_settings.test_db

    assert "test_" in test_db_name, "Защита от выполнения create/drop с основной БД"

    engine_for_create_db: Engine = create_engine(
        str(postgres_settings.db_url),
        echo=False,
        isolation_level="AUTOCOMMIT",
    )

    connection_for_create_test_db = engine_for_create_db.connect()

    is_test_db_exists = connection_for_create_test_db.execute(
        stmt_check_database, {"test_db_name": test_db_name}
    )

    if not is_test_db_exists.one_or_none():
        connection_for_create_test_db.execute(
            query_create_database,
            {"test_db_name": test_db_name},
        )
    if engine_for_create_db:
        engine_for_create_db.dispose()
    connection_for_create_test_db.close()

    return create_engine(postgres_settings.test_url)


@pytest.fixture(scope="session")
def drop_tables(
    engine: Engine,
    postgres_settings: PostgreSQLSettings,
) -> Generator[None]:
    yield
    query_drop_database = text("DROP DATABASE :test_db_name")
    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        connection.execute(
            query_drop_database,
            {"test_db_name": postgres_settings.test_db},
        )


@pytest.fixture(scope="session")
def database(postgres_settings: PostgreSQLSettings) -> Database:
    return Database(url=postgres_settings.test_url)


@pytest.fixture(scope="session")
def orm_notes_repository(database: Database) -> INotesRepository:
    return ORMNotesRepository(database=database)


@pytest.fixture(scope="session")
def diary(orm_notes_repository: INotesRepository) -> Diary:
    return Diary(repository=orm_notes_repository)


@pytest.fixture
def orm_user(database: Database, user_oid: str) -> ORMUser:
    user = ORMUser(
        oid=UUID(user_oid),
        username="test_user",
        password=b"test_password",
    )

    with database.get_session() as session:
        session = cast(Session, session)
        query_delete_user = delete(ORMUser).where(ORMUser.username == user.username)
        session.execute(query_delete_user)

        session.add(user)
        session.commit()
        session.refresh(user)

    return user
