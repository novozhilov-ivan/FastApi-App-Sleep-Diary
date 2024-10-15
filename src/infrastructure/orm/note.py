from datetime import date, time
from typing_extensions import Self
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities.note import NoteEntity
from src.domain.values.points import Points
from src.infrastructure.orm.base import ORMBase
from src.infrastructure.orm.mixins import MixinMetaInfo


class ORMNote(ORMBase, MixinMetaInfo):
    __tablename__ = "notes"
    __table_args__ = (
        UniqueConstraint(
            "bedtime_date",
            "owner_oid",
            name="unique_bedtime_date_for_user",
        ),
    )
    bedtime_date: Mapped[date]
    went_to_bed: Mapped[time]
    fell_asleep: Mapped[time]
    woke_up: Mapped[time]
    got_up: Mapped[time]
    no_sleep: Mapped[time]
    owner_oid: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="users.oid",
            ondelete="CASCADE",
        ),
    )

    @classmethod
    def from_entity(cls: type["ORMNote"], obj: NoteEntity) -> "ORMNote":
        return cls(
            bedtime_date=obj.points.bedtime_date,
            went_to_bed=obj.points.went_to_bed,
            fell_asleep=obj.points.fell_asleep,
            woke_up=obj.points.woke_up,
            got_up=obj.points.got_up,
            no_sleep=obj.points.no_sleep,
            owner_oid=obj.owner_oid,
        )

    def to_entity(self: Self) -> NoteEntity:
        return NoteEntity(
            oid=self.oid,
            created_at=self.created_at,
            updated_at=self.updated_at,
            owner_oid=self.owner_oid,
            points=Points(
                bedtime_date=self.bedtime_date,
                went_to_bed=self.went_to_bed.replace(tzinfo=None),
                fell_asleep=self.fell_asleep.replace(tzinfo=None),
                woke_up=self.woke_up.replace(tzinfo=None),
                got_up=self.got_up.replace(tzinfo=None),
                no_sleep=self.no_sleep.replace(tzinfo=None),
            ),
        )

    def __repr__(self: Self) -> str:
        return (
            f"<NoteORM "
            f"oid='{str(self.oid)[:3]}...{str(self.oid)[-3:]}' "
            f"date='{self.bedtime_date}' "
            f"owner_oid='{str(self.owner_oid)[:3]}...{str(self.owner_oid)[-3:]}'>"
        )
