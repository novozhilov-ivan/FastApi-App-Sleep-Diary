from uuid import UUID

from src import domain
from src.domain.note import NoteTimePoints
from src.infrastructure.repository.base import IDiaryRepository


def write(
    bedtime_date: str,
    went_to_bed: str,
    fell_asleep: str,
    woke_up: str,
    got_up: str,
    no_sleep: str | None,
    owner_id: UUID,
    repo: IDiaryRepository,
) -> None:
    diary = repo.get_diary(owner_id)
    domain.write(
        NoteTimePoints(
            bedtime_date=bedtime_date,
            went_to_bed=went_to_bed,
            fell_asleep=fell_asleep,
            woke_up=woke_up,
            got_up=got_up,
            no_sleep=no_sleep or "00:00",
        ),
        diary,
    )
