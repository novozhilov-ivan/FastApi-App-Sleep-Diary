from datetime import date, time
from uuid import UUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.orm.mixins import MetaInfo


class NoteORM(MetaInfo):
    __tablename__ = "sleep_note"
    __table_args__ = (
        UniqueConstraint(
            "sleep_date",
            "owner_id",
            name="unique_sleep_date_for_user",
        ),
    )

    sleep_date: Mapped[date]
    went_to_bed: Mapped[time]
    fell_asleep: Mapped[time]
    woke_up: Mapped[time]
    got_up: Mapped[time]
    no_sleep: Mapped[time]

    owner_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            column="user.id",
            ondelete="CASCADE",
        ),
    )
