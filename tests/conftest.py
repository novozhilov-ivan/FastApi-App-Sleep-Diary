import io
from collections.abc import Generator, Iterable
from datetime import date, time
from itertools import chain
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from dishka import Container
from sqlalchemy import Engine, create_engine, text

from src.application.api.sleep_diary.services.diary import Diary
from src.domain.sleep_diary.entities.user import UserEntity
from src.domain.sleep_diary.services.base import INotesRepository
from src.domain.sleep_diary.values.points import Points
from src.gateways.postgresql.database import Database
from src.gateways.postgresql.models import ORMUser
from src.infra.sleep_diary.repository.orm_notes import ORMNotesRepository
from src.project.containers import get_test_container
from src.project.settings import PostgreSQLSettings

STMT_CHECK_DATABASE = "SELECT 1 FROM pg_database WHERE datname = :test_db_name;"


@pytest.fixture(scope="session")
def test_container() -> Container:
    return get_test_container()


@pytest.fixture(scope="session")
def user_oid() -> str:
    return str(uuid4())


@pytest.fixture(scope="session")
def username() -> str:
    return "test_user"


@pytest.fixture(scope="session")
def plain_password() -> str:
    return "test_password"


@pytest.fixture(scope="session")
def user_entity(
    user_oid: str,
    username: str,
    plain_password: str,
) -> UserEntity:
    return UserEntity(
        oid=UUID(user_oid),
        username=username,
        password=plain_password,
    )


@pytest.fixture(scope="session")
def postgres_settings(test_container: Container) -> PostgreSQLSettings:
    return test_container.get(PostgreSQLSettings)


@pytest.fixture(scope="session")
def alembic_test_config(
    postgres_settings: PostgreSQLSettings,
) -> AlembicConfig:
    base_dir = Path(__file__).parent.parent
    alembic_ini = base_dir / "src" / "alembic.ini"

    stdout = io.StringIO("")
    alembic_config = AlembicConfig(str(alembic_ini), stdout=stdout)
    alembic_config.set_main_option("sqlalchemy.url", postgres_settings.test_url)

    return alembic_config


@pytest.fixture(scope="session")
def test_db_engine(
    postgres_settings: PostgreSQLSettings,
    alembic_test_config: AlembicConfig,
) -> Generator[Engine, None, None]:
    test_db_name = postgres_settings.test_db
    test_db_url = postgres_settings.test_url

    assert "test_" in test_db_name, "Защита от выполнения create/drop с основной БД"
    assert "test_" in test_db_url, "Защита от выполнения create/drop с основной БД"

    engine_for_create_db: Engine = create_engine(
        url=postgres_settings.db_url,
        echo=False,
        isolation_level="AUTOCOMMIT",
    )
    with engine_for_create_db.connect() as connection:
        is_test_db_exists = connection.execute(
            text(STMT_CHECK_DATABASE),
            {"test_db_name": test_db_name},
        ).scalar()

        if not is_test_db_exists:
            connection.execute(text(f"CREATE DATABASE {test_db_name}"))
    engine_for_create_db.dispose()

    upgrade(alembic_test_config, "head")
    engine = create_engine(test_db_url)
    try:
        yield engine
    finally:
        engine.dispose()


@pytest.fixture(scope="session")
def database(
    test_container: Container,
) -> Database:
    return test_container.get(Database)


@pytest.fixture(autouse=True)
def cleanup_tables_test(test_db_engine: Engine) -> Generator[None, None, None]:
    select_all_tables = (
        "SELECT tablename FROM pg_tables"
        " WHERE schemaname = 'public'"
        " AND tablename NOT LIKE 'alembic_%'"
        " ORDER BY tablename DESC"
    )
    with test_db_engine.begin() as conn:
        for (table_name,) in conn.execute(text(select_all_tables)).fetchall():
            conn.execute(text(f"DELETE FROM {table_name}"))

    try:
        yield
    finally:
        with test_db_engine.begin() as conn:
            for (table_name,) in conn.execute(text(select_all_tables)).fetchall():
                conn.execute(text(f"DELETE FROM {table_name}"))


@pytest.fixture
def orm_user(
    database: Database,
    user_oid: str,
    username: str,
    plain_password: str,
) -> ORMUser:
    user = ORMUser(
        oid=UUID(user_oid),
        username=username,
        password=plain_password,
    )
    with database.get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)

    return user


@pytest.fixture(scope="session")
def orm_notes_repository(database: Database) -> INotesRepository:
    return ORMNotesRepository(database=database)


@pytest.fixture(scope="session")
def diary_with_orm(orm_notes_repository: INotesRepository) -> Diary:
    return Diary(repository=orm_notes_repository)


date_point: date = date(2020, 12, 12)

type T = tuple[date, time, time, time, time]
type TT = tuple[T, T, T, T]
# 4 Корректных, последовательных и отсортированных данных для временных точек.
# Все имеют:
# 8 часов сна [fell_asleep:woke_up]
# 2 часа между отходом ко сну и засыпанием [went_to_bed:fell_asleep]
# 2 часа между  пробуждением и подъемом [woke_up:got_up]
# 12 часов между отходом ко сну и подъемом [went_to_bed:got_up]
# Время без сна отсутствует
points_order_desc_from_went_to_bed: T = (
    date_point,
    time(1),
    time(3),
    time(11),
    time(13),
)
points_order_desc_from_got_up: T = (
    date_point,
    time(13),
    time(15),
    time(23),
    time(1),
)
points_order_desc_from_woke_up: T = (
    date_point,
    time(15),
    time(17),
    time(1),
    time(3),
)
points_order_desc_from_fell_asleep: T = (
    date_point,
    time(23),
    time(1),
    time(9),
    time(11),
)
correct_points_4_different_order_of_sequences: TT = (
    points_order_desc_from_went_to_bed,
    points_order_desc_from_got_up,
    points_order_desc_from_woke_up,
    points_order_desc_from_fell_asleep,
)

# went_to_bed is wrong
wrong_points_went_to_bed_gt_fell_asleep_and_lt_other_time_points: T = (
    date_point,
    time(4),
    time(3),
    time(12),
    time(14),
)
wrong_points_went_to_bed_gt_fell_asleep_with_points_after_midnight: T = (
    date_point,
    time(14),
    time(13),
    time(2),
    time(4),
)
wrong_points_went_to_bed_gt_fell_asleep_and_woke_up: T = (
    date_point,
    time(12),
    time(3),
    time(11),
    time(13),
)
wrong_points_went_to_bed_gt_woke_up_and_lt_others_points: T = (
    date_point,
    time(8),
    time(23),
    time(7),
    time(9),
)
wrong_points_where_went_to_bed_is_wrong: TT = (
    wrong_points_went_to_bed_gt_fell_asleep_and_lt_other_time_points,
    wrong_points_went_to_bed_gt_fell_asleep_with_points_after_midnight,
    wrong_points_went_to_bed_gt_fell_asleep_and_woke_up,
    wrong_points_went_to_bed_gt_woke_up_and_lt_others_points,
)
# fell_asleep is wrong
wrong_points_fell_asleep_gt_wok_up_and_lt_got_up: T = (
    date_point,
    time(1),
    time(12),
    time(11),
    time(13),
)
wrong_points_fell_asleep_gt_got_up_and_got_up_lt_went_to_bed: T = (
    date_point,
    time(1),
    time(14),
    time(11),
    time(13),
)
wrong_points_fell_asleep_gt_woke_up_and_lt_went_to_bed: T = (
    date_point,
    time(23),
    time(10),
    time(9),
    time(11),
)
wrong_points_fell_asleep_gt_got_up_and_lt_went_to_bed: T = (
    date_point,
    time(23),
    time(12),
    time(9),
    time(11),
)
wrong_points_where_fell_asleep_is_wrong: TT = (
    wrong_points_fell_asleep_gt_wok_up_and_lt_got_up,
    wrong_points_fell_asleep_gt_got_up_and_got_up_lt_went_to_bed,
    wrong_points_fell_asleep_gt_woke_up_and_lt_went_to_bed,
    wrong_points_fell_asleep_gt_got_up_and_lt_went_to_bed,
)
# woke_up is wrong
wrong_points_woke_up_gt_got_up_while_got_up_gt_other_points: T = (
    date_point,
    time(1),
    time(3),
    time(14),
    time(13),
)
wrong_points_woke_up_gt_got_up_while_got_up_gt_fell_asleep_and_lt_went_to_bed: T = (
    date_point,
    time(23),
    time(1),
    time(12),
    time(11),
)
wrong_points_woke_up_gt_got_up_and_lt_other_points: T = (
    date_point,
    time(13),
    time(15),
    time(2),
    time(1),
)
wrong_points_woke_up_lt_other_points: T = (
    date_point,
    time(13),
    time(15),
    time(1),
    time(23),
)
wrong_points_where_woke_up_is_wrong: TT = (
    wrong_points_woke_up_gt_got_up_while_got_up_gt_other_points,
    wrong_points_woke_up_gt_got_up_while_got_up_gt_fell_asleep_and_lt_went_to_bed,
    wrong_points_woke_up_gt_got_up_and_lt_other_points,
    wrong_points_woke_up_lt_other_points,
)
# got up is wrong
wrong_points_got_up_lt_woke_up_and_gt_other_points: T = (
    date_point,
    time(1),
    time(3),
    time(11),
    time(10),
)
wrong_points_got_up_gt_fell_asleep_and_lt_other_points: T = (
    date_point,
    time(23),
    time(1),
    time(7),
    time(6),
)
wrong_points_got_up_lt_woke_up_while_woke_up_lt_other_points: T = (
    date_point,
    time(15),
    time(17),
    time(2),
    time(1),
)
wrong_points_got_up_lt_fell_asleep_and_gt_other_points: T = (
    date_point,
    time(21),
    time(23),
    time(7),
    time(22),
)
wrong_points_where_got_up_is_wrong: TT = (
    wrong_points_got_up_lt_woke_up_and_gt_other_points,
    wrong_points_got_up_gt_fell_asleep_and_lt_other_points,
    wrong_points_got_up_lt_woke_up_while_woke_up_lt_other_points,
    wrong_points_got_up_lt_fell_asleep_and_gt_other_points,
)
# Все point'ы, в которых не корректная сортировка
all_wrong_points_sequences: Iterable[T] = chain.from_iterable(
    (
        wrong_points_where_went_to_bed_is_wrong,
        wrong_points_where_fell_asleep_is_wrong,
        wrong_points_where_woke_up_is_wrong,
        wrong_points_where_got_up_is_wrong,
    ),
)
#  Point'ы, в которых время без сна больше времени сна
type TN = tuple[date, time, time, time, time, time]
type TTN = tuple[TN, TN, TN, TN]
wrong_points_no_sleep_gt_sleep_order_asc_from_went_to_bed: TN = (
    date_point,
    time(1),
    time(3),
    time(11),
    time(13),
    time(9),
)
wrong_points_no_sleep_gt_sleep_order_asc_from_got_up: TN = (
    date_point,
    time(13),
    time(15),
    time(23),
    time(1),
    time(9),
)
wrong_points_no_sleep_gt_sleep_order_asc_from_woke_up: TN = (
    date_point,
    time(15),
    time(17),
    time(1),
    time(3),
    time(9),
)
wrong_points_no_sleep_gt_sleep_order_asc_from_fell_asleep: TN = (
    date_point,
    time(23),
    time(1),
    time(9),
    time(11),
    time(9),
)
wrong_points_where_no_sleep_gt_sleep: TTN = (
    wrong_points_no_sleep_gt_sleep_order_asc_from_went_to_bed,
    wrong_points_no_sleep_gt_sleep_order_asc_from_got_up,
    wrong_points_no_sleep_gt_sleep_order_asc_from_woke_up,
    wrong_points_no_sleep_gt_sleep_order_asc_from_fell_asleep,
)
# Временные точки с нулевыми значениями
points_all_zero: T = (
    date_point,
    time(),
    time(),
    time(),
    time(),
)
points_with_zeros_and_some_big_no_sleep: TN = (
    date_point,
    time(),
    time(),
    time(),
    time(),
    time(10),
)
# Корректные временные точки с разными последовательностями и 1 часов без сна
points_order_desc_from_went_to_bed_and_one_hour_no_sleep: TN = (
    date_point,
    time(1),
    time(3),
    time(11),
    time(13),
    time(1),
)
points_order_desc_from_got_up_and_one_hour_no_sleep: TN = (
    date_point,
    time(13),
    time(15),
    time(23),
    time(1),
    time(1),
)
points_order_desc_from_woke_up_and_one_hour_no_sleep: TN = (
    date_point,
    time(15),
    time(17),
    time(1),
    time(3),
    time(1),
)
points_order_desc_from_fell_asleep_and_one_hour_no_sleep: TN = (
    date_point,
    time(23),
    time(1),
    time(9),
    time(11),
    time(1),
)
correct_points_4_different_order_of_sequences_and_one_hour_no_sleep: TTN = (
    points_order_desc_from_went_to_bed_and_one_hour_no_sleep,
    points_order_desc_from_got_up_and_one_hour_no_sleep,
    points_order_desc_from_woke_up_and_one_hour_no_sleep,
    points_order_desc_from_fell_asleep_and_one_hour_no_sleep,
)

all_correct_points_sequences: list[Points] = [
    Points(*points) for points in correct_points_4_different_order_of_sequences
]
