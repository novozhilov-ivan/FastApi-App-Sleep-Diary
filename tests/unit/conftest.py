from typing_extensions import Self

import pytest

from src.domain.values.points import Points
from src.infra.repository import BaseNotesRepository, MemoryNotesRepository
from src.service_layer import Diary


class FakePoints(Points):
    def validate(self: Self) -> None: ...


@pytest.fixture
def notes_repository() -> BaseNotesRepository:
    return MemoryNotesRepository()


@pytest.fixture
def diary(notes_repository: BaseNotesRepository) -> Diary:
    return Diary(notes_repository)
