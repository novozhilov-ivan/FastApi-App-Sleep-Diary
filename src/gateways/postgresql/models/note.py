from datetime import date, time
from uuid import UUID

from sqlalchemy import ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.sleep_diary.entities.note import NoteEntity
from src.domain.sleep_diary.values.points import Points
from src.gateways.postgresql.models.base import ORMBase
from src.gateways.postgresql.models.mixins import MixinUpdatedAt, MixinUUIDOid


class ORMNote(ORMBase, MixinUUIDOid, MixinUpdatedAt):
    __tablename__ = "notes"
    __table_args__ = (
        PrimaryKeyConstraint(
            "bedtime_date",
            "owner_oid",
            name="unique_bedtime_date_for_user",
        ),
    )

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
            created_at=obj.created_at,
            updated_at=obj.updated_at,
            bedtime_date=obj.points.bedtime_date,
            went_to_bed=obj.points.went_to_bed,
            fell_asleep=obj.points.fell_asleep,
            woke_up=obj.points.woke_up,
            got_up=obj.points.got_up,
            no_sleep=obj.points.no_sleep,
        )

    def to_entity(self) -> NoteEntity:
        return NoteEntity(
            oid=self.oid,
            owner_oid=self.owner_oid,
            created_at=self.created_date,
            updated_at=self.updated_date,
            points=Points(
                self.bedtime_date,
                self.went_to_bed.replace(tzinfo=None),
                self.fell_asleep.replace(tzinfo=None),
                self.woke_up.replace(tzinfo=None),
                self.got_up.replace(tzinfo=None),
                self.no_sleep.replace(tzinfo=None),
            ),
        )

    def __repr__(self) -> str:
        return (
            f"<NoteORM "
            f"oid='{str(self.oid)[:4]}...' "
            f"bedtime_date='{self.bedtime_date}' "
            f"owner_oid='{str(self.owner_oid)[:4]}...' "
        )
