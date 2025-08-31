import pytest

from src.domain.sleep_diary.entities.user import UserEntity
from src.domain.sleep_diary.services.base import INotesRepository
from src.infra.identity.services.authentication import UserAuthenticationService
from src.infra.sleep_diary.repository.memory_notes import MemoryNotesRepository
from src.infra.sleep_diary.repository.memory_users import MemoryUsersRepository
from src.infra.sleep_diary.use_cases.diary import Diary


@pytest.fixture(scope="session")
def username() -> str:
    return "correct_username"


@pytest.fixture(scope="session")
def plain_password() -> str:
    return "correct_password"


@pytest.fixture(scope="session")
def created_user(username: str, plain_password: str) -> UserEntity:
    return UserEntity(username=username, password=plain_password)


@pytest.fixture(scope="session")
def created_user_with_hashed_password(
    username: str,
    plain_password: str,
) -> UserEntity:
    return UserEntity(
        username=username,
        password=UserAuthenticationService.hash_password(plain_password),
    )


@pytest.fixture
def user_repository() -> MemoryUsersRepository:
    return MemoryUsersRepository()


@pytest.fixture
def notes_repository() -> MemoryNotesRepository:
    return MemoryNotesRepository()


@pytest.fixture
def diary(notes_repository: INotesRepository) -> Diary:
    return Diary(notes_repository)
