import pytest

from punq import Container, Scope

from src.infrastructure.repository import BaseDiaryRepository
from src.infrastructure.repository.memory import MemoryDiaryRepository
from src.project.containers import get_container
from src.service_layer import Diary


def init_dummy_container() -> Container:
    container = get_container()

    container.register(
        BaseDiaryRepository,
        MemoryDiaryRepository,
        scope=Scope.singleton,
    )
    repository: BaseDiaryRepository = container.resolve(BaseDiaryRepository)

    container.register(
        Diary,
        factory=lambda: Diary(repository),
        scope=Scope.singleton,
    )

    return container


@pytest.fixture
def container() -> Container:
    return init_dummy_container()


@pytest.fixture
def diary_repository(container: Container) -> BaseDiaryRepository:
    return container.resolve(BaseDiaryRepository)


@pytest.fixture
def diary(container: Container) -> Diary:
    return container.resolve(Diary)
