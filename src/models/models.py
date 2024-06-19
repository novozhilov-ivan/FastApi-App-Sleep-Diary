from datetime import date, datetime, time

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from src.extension import Base


class MetaInfoBaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.utcnow(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )


class SleepNoteOrm(MetaInfoBaseModel):
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
    owner_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="user.id",
            ondelete="CASCADE",
        ),
    )


class UserOrm(MetaInfoBaseModel):
    __tablename__ = "user"
    username: Mapped[str] = mapped_column(
        unique=True,
    )
    password: Mapped[str]
