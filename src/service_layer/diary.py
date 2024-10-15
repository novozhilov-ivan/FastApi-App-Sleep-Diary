from dataclasses import dataclass
from datetime import date, time
from typing_extensions import Self

from src.domain import services
from src.domain.entities.note import NoteEntity
from src.domain.exceptions import NonUniqueNoteBedtimeDateException
from src.domain.values.points import Points
from src.infrastructure.repository.base import INoteRepository, IUserRepository


@dataclass(kw_only=True)
class Diary:
    user_repository: IUserRepository
    notes_repository: INoteRepository

    def write(
        self: Self,
        bedtime_date: date,
        went_to_bed: time,
        fell_asleep: time,
        woke_up: time,
        got_up: time,
        no_sleep: time,
    ) -> None:
        note = NoteEntity(
            owner_oid=self.user_repository.oid,
            points=Points(
                bedtime_date=bedtime_date,
                went_to_bed=went_to_bed,
                fell_asleep=fell_asleep,
                woke_up=woke_up,
                got_up=got_up,
                no_sleep=no_sleep,
            ),
        )
        diary = services.Diary.create(
            self.notes_repository.get_all(self.user_repository.oid),
        )
        if not diary.can_write(note):
            raise NonUniqueNoteBedtimeDateException(
                bedtime_date=note.points.bedtime_date,
            )
        diary.write(note)
        self.notes_repository.add(note)
