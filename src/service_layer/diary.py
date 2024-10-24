from dataclasses import dataclass
from datetime import date, time
from typing_extensions import Self
from uuid import UUID

from src.domain import services
from src.domain.entities.note import NoteEntity
from src.domain.exceptions import NonUniqueNoteBedtimeDateException
from src.domain.values.points import Points
from src.infrastructure.repository.base import BaseDiaryRepository


@dataclass
class Diary:
    repository: BaseDiaryRepository

    # user_service: InitVar[UserAuthenticationService]
    # owner_oid: UUID = field(init=False)
    #
    # def __post_init__(self: Self, user_service: UserAuthenticationService) -> None:
    #     self.owner_oid = user_service.user.oid

    def write(
        self: Self,
        owner_oid: UUID,
        bedtime_date: date,
        went_to_bed: time,
        fell_asleep: time,
        woke_up: time,
        got_up: time,
        no_sleep: time | None = None,
    ) -> None:
        note = NoteEntity(
            owner_oid=owner_oid,
            points=Points(
                bedtime_date=bedtime_date,
                went_to_bed=went_to_bed,
                fell_asleep=fell_asleep,
                woke_up=woke_up,
                got_up=got_up,
                no_sleep=no_sleep or time(),
            ),
        )
        diary = services.DiaryService.create(
            notes=self.repository.get_all_notes(owner_oid),
        )

        if not diary.can_write(note):
            raise NonUniqueNoteBedtimeDateException(note.points.bedtime_date)

        diary.write(note)
        self.repository.add(note)
