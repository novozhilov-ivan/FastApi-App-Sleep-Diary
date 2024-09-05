from uuid import UUID

from src import domain
from src.domain.note import NoteTimePoints
from src.infrastructure.repository.base import BaseDiaryRepository


def write(
    bedtime_date: str,
    went_to_bed: str,
    fell_asleep: str,
    woke_up: str,
    got_up: str,
    no_sleep: str | None,
    owner_oid: UUID,
    repository: BaseDiaryRepository,
) -> None:
    note = NoteTimePoints(
        bedtime_date=bedtime_date,
        went_to_bed=went_to_bed,
        fell_asleep=fell_asleep,
        woke_up=woke_up,
        got_up=got_up,
        no_sleep=no_sleep or "00:00",
    )
    diary = repository.get_diary(owner_oid)
    new_note = domain.write(note, diary)
    repository.add(new_note, owner_oid)
