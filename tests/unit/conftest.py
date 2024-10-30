from typing_extensions import Self

import pytest

from src.domain.services import INotesRepository, IUsersRepository
from src.domain.values.points import Points
from src.infra.repository import MemoryNotesRepository, MemoryUsersRepository
from src.service_layer import Diary
from src.service_layer.services import (
    IUserAuthenticationService,
    UserAuthenticationService,
)


class FakePoints(Points):
    def validate(self: Self) -> None: ...


@pytest.fixture
def notes_repository() -> INotesRepository:
    return MemoryNotesRepository()


@pytest.fixture
def user_repository() -> IUsersRepository:
    return MemoryUsersRepository()


@pytest.fixture
def authentication_service(
    user_repository: IUsersRepository,
) -> IUserAuthenticationService:
    return UserAuthenticationService(user_repository)


@pytest.fixture
def diary(notes_repository: INotesRepository) -> Diary:
    return Diary(notes_repository)
