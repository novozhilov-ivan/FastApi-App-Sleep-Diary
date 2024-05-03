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
from sqlalchemy.orm import backref, relationship

from api.extension import db


class Notation(db.Model):
    __tablename__ = "notation"
    id = Column(Integer, primary_key=True)
    calendar_date = Column(Date, nullable=False)
    bedtime = Column(Time, nullable=False)
    asleep = Column(Time, nullable=False)
    awake = Column(Time, nullable=False)
    rise = Column(Time, nullable=False)
    without_sleep = Column(Time, name="without_sleep", nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    user = relationship("User", lazy=True, backref=backref("notations", lazy=True))

    __table_args__ = (
        UniqueConstraint(
            "calendar_date", "user_id", name="uniq_calendar_date_for_user"
        ),
    )

    # Todo прописать on_delete действие. При удалении пользователя - что происходит с записями дневника?
    def __repr__(self):
        return (
            f"Запись в дневнике: [ID: {self.id}, ДАТА: {self.calendar_date}, ID"
            f" ВЛАДЕЛЬЦА: {self.user_id}]"
        )


class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    login = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    date_of_registration = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Пользователь [ID: {self.login}, LOGIN: {self.login}]"
