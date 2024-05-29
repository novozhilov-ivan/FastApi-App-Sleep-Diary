from datetime import datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from api.extension import db


class DreamNote(db.Model):
    __tablename__ = "dream_note"
    __table_args__ = (
        UniqueConstraint(
            "sleep_date",
            "user_id",
            name="uniq_sleep_date_for_user",
        ),
    )
    id = Column(Integer, primary_key=True)
    sleep_date = Column(Date, nullable=False)
    went_to_bed = Column(Time, nullable=False)
    fell_asleep = Column(Time, nullable=False)
    woke_up = Column(Time, nullable=False)
    got_up = Column(Time, nullable=False)
    no_sleep = Column(Time, nullable=False)
    user_id = Column(
        Integer,
        ForeignKey("user.id"),
        nullable=False,
    )

    def __repr__(self):
        return (
            f"Запись в дневнике: "
            f"["
            f"ID: {self.id}, "
            f"ДАТА: {self.sleep_date}, "
            f"ID ВЛАДЕЛЬЦА: {self.user_id}, "
            f"]"
        )


class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    registration_date = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
    )
    dream_notes = relationship(
        "DreamNote",
        backref="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"Пользователь [ID: {self.id}, LOGIN: {self.username}]"
