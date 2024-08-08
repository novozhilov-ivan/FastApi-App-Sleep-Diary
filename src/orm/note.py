from datetime import date, time

from sqlalchemy.orm import Mapped

from src.orm.base import BaseORM
from src.orm.mixins import MetaInfo


class NoteORM(BaseORM, MetaInfo):
    __tablename__ = "notes"
    # __table_args__ = (
    #     UniqueConstraint(
    #         "bedtime_date",
    #         "owner_id",
    #         name="unique_bedtime_date_for_user",
    #     ),
    # )

    bedtime_date: Mapped[date]
    went_to_bed: Mapped[time]
    fell_asleep: Mapped[time]
    woke_up: Mapped[time]
    got_up: Mapped[time]
    no_sleep: Mapped[time]

    # owner_id: Mapped[UUID] = mapped_column(
    #     ForeignKey(
    #         column="users.oid",
    #         ondelete="CASCADE",
    #     ),
    # )
