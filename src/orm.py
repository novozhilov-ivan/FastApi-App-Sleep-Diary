import datetime as dt

from sqlalchemy import (
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from src.extension import Base


class MetaInfoBaseModel(Base):
    __abstract__ = True

    oid: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        unique=True,
    )
    created_at: Mapped[dt.datetime] = mapped_column(
        default=lambda: dt.datetime.now(tz=dt.UTC),
    )
    updated_at: Mapped[dt.datetime] = mapped_column(
        default=lambda: dt.datetime.now(tz=dt.UTC),
        onupdate=lambda: dt.datetime.now(tz=dt.UTC),
    )


class Note(MetaInfoBaseModel):
    __tablename__ = "sleep_note"
    __table_args__ = (
        UniqueConstraint(
            "sleep_date",
            "owner_id",
            name="unique_sleep_date_for_user",
        ),
    )

    sleep_date: Mapped[dt.date]
    went_to_bed: Mapped[dt.time]
    fell_asleep: Mapped[dt.time]
    woke_up: Mapped[dt.time]
    got_up: Mapped[dt.time]
    no_sleep: Mapped[dt.time]

    owner_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="user.id",
            ondelete="CASCADE",
        ),
    )


class User(MetaInfoBaseModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
