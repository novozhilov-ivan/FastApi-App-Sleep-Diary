from typing_extensions import Self

import pytest

from src.domain.values.points import Points
from src.infra.repository import INotesRepository, MemoryNotesRepository
from src.service_layer import Diary


class FakePoints(Points):
    def validate(self: Self) -> None: ...


@pytest.fixture
def notes_repository() -> INotesRepository:
    return MemoryNotesRepository()


@pytest.fixture
def diary(notes_repository: INotesRepository) -> Diary:
    return Diary(notes_repository)
