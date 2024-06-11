from datetime import date, datetime, time
from typing import Annotated

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from api.extension import Base

# TODO сделать абстрактные дочерние классы Base

intpk = Annotated[
    int,
    mapped_column(
        primary_key=True,
    ),
]
created_at_type = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    ),
]
updated_at_type = Annotated[
    datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow,
    ),
]


class DreamNote(Base):
    __tablename__ = "dream_note"
    __table_args__ = (
        UniqueConstraint(
            "sleep_date",
            "user_id",
            name="unique_sleep_date_for_user",
        ),
    )
    id: Mapped[intpk]
    sleep_date: Mapped[date]
    went_to_bed: Mapped[time]
    fell_asleep: Mapped[time]
    woke_up: Mapped[time]
    got_up: Mapped[time]
    no_sleep: Mapped[time]
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column="user.id",
            ondelete="CASCADE",
        ),
    )
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]


class User(Base):
    __tablename__ = "user"
    id: Mapped[intpk]
    username: Mapped[str] = mapped_column(
        unique=True,
    )
    password: Mapped[str]
    registration_date: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    )
    created_at: Mapped[created_at_type]
    updated_at: Mapped[updated_at_type]
