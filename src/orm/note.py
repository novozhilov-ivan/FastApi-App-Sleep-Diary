from datetime import date, time
from typing import Type
from typing_extensions import Self
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.note import NoteEntity, NoteTimePoints
from src.orm.base import BaseORM
from src.orm.mixins import MixinMetaInfo


class NoteORM(BaseORM, MixinMetaInfo):
    __tablename__ = "notes"
    __table_args__ = (
        UniqueConstraint(
            "bedtime_date",
            "owner_id",
            name="unique_bedtime_date_for_user",
        ),
    )
    bedtime_date: Mapped[date]
    went_to_bed: Mapped[time]
    fell_asleep: Mapped[time]
    woke_up: Mapped[time]
    got_up: Mapped[time]
    no_sleep: Mapped[time]
    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="users.oid",
            ondelete="CASCADE",
        ),
    )

    @classmethod
    def from_time_points(cls: Type["NoteORM"], obj: NoteTimePoints) -> "NoteORM":
        return cls(
            bedtime_date=obj.bedtime_date,
            went_to_bed=obj.went_to_bed,
            fell_asleep=obj.fell_asleep,
            woke_up=obj.woke_up,
            got_up=obj.got_up,
            no_sleep=obj.no_sleep,
        )

    def to_entity(self: Self) -> NoteEntity:
        return NoteEntity(
            oid=self.oid,
            created_at=self.created_at,
            updated_at=self.updated_at,
            bedtime_date=self.bedtime_date,
            went_to_bed=self.went_to_bed.replace(tzinfo=None),
            fell_asleep=self.fell_asleep.replace(tzinfo=None),
            woke_up=self.woke_up.replace(tzinfo=None),
            got_up=self.got_up.replace(tzinfo=None),
            no_sleep=self.no_sleep.replace(tzinfo=None),
        )

    def __repr__(self: Self) -> str:
        return (
            f"<NoteORM "
            f"oid='{str(self.oid)[:3]}...{str(self.oid)[-3:]}' "
            f"date='{self.bedtime_date}'>"
        )
