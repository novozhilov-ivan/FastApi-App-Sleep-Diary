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
    __table_args__ = (
        UniqueConstraint(
            "bedtime_date",
            "owner_oid",
            name="unique_bedtime_date_for_user",
        ),
    )
    # TODO Сделать 'bedtime_date' и 'owner_oid' - PK
    #  Схема таблицы будет соответствовать 3НФ или БКНФ
    #  (не ключевые атрибуты зависят полностью от первичного ключа)
    #  oid лишить PK и оставить unique

    bedtime_date: Mapped[date]
    owner_oid: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="users.oid",
            ondelete="CASCADE",
        ),
    )
    went_to_bed: Mapped[time]
    fell_asleep: Mapped[time]
    woke_up: Mapped[time]
    got_up: Mapped[time]
    no_sleep: Mapped[time]

    @classmethod
    def from_entity(cls: type["ORMNote"], obj: NoteEntity) -> "ORMNote":
        return cls(
            oid=obj.oid,
            owner_oid=obj.owner_oid,
            bedtime_date=obj.points.bedtime_date,
            went_to_bed=obj.points.went_to_bed,
            fell_asleep=obj.points.fell_asleep,
            woke_up=obj.points.woke_up,
            got_up=obj.points.got_up,
            no_sleep=obj.points.no_sleep,
        )

    def to_entity(self: Self) -> NoteEntity:
        return NoteEntity(
            owner_oid=self.owner_oid,
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
            f"oid='{str(self.oid)[:4]}...' "
            f"bedtime_date='{self.bedtime_date}' "
            f"owner_oid='{str(self.owner_oid)[:4]}...' "
        )
