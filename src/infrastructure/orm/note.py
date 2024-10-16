from datetime import date, time
from typing_extensions import Self
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities.note import NoteEntity
from src.domain.values.points import Points
from src.infrastructure.orm.base import ORMBase
from src.infrastructure.orm.mixins import MixinUUIDOid


class ORMNote(ORMBase, MixinUUIDOid):
    __tablename__ = "notes"
    bedtime_date: Mapped[date]
    went_to_bed: Mapped[time]
    fell_asleep: Mapped[time]
    woke_up: Mapped[time]
    got_up: Mapped[time]
    no_sleep: Mapped[time]

    # TODO переместить в отдельную таблицу
    #  <ORMUsersNotes(oid: UUID, note_oid:UUID, user_oid:UUID)>
    #  user_oid - ForeignKey
    #  note_oid - ForeignKey
    #  или
    #  note_bedtime_date и user_oid - ForeignKey's и их комбинация - UniqueConstraint
    owner_oid: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="users.oid",
            ondelete="CASCADE",
        ),
    )
    # TODO перенести в отдельную таблицу
    __table_args__ = (
        UniqueConstraint(
            "bedtime_date",
            "owner_oid",
            name="unique_bedtime_date_for_user",
        ),
    )

    @classmethod
    def from_entity(cls: type["ORMNote"], obj: NoteEntity) -> "ORMNote":
        return cls(
            oid=obj.oid,
            bedtime_date=obj.points.bedtime_date,
            went_to_bed=obj.points.went_to_bed,
            fell_asleep=obj.points.fell_asleep,
            woke_up=obj.points.woke_up,
            got_up=obj.points.got_up,
            no_sleep=obj.points.no_sleep,
        )

    def to_entity(self: Self) -> NoteEntity:
        return NoteEntity(
            oid=self.oid,
            points=Points(
                self.bedtime_date,
                self.went_to_bed.replace(tzinfo=None),
                self.fell_asleep.replace(tzinfo=None),
                self.woke_up.replace(tzinfo=None),
                self.got_up.replace(tzinfo=None),
                self.no_sleep.replace(tzinfo=None),
            ),
        )

    def __repr__(self: Self) -> str:
        return (
            f"<NoteORM "
            f"oid='{str(self.oid)[:3]}...{str(self.oid)[-3:]}' "
            f"date='{self.bedtime_date}' "
        )
