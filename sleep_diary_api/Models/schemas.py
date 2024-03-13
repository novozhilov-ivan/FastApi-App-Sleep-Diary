from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

from sleep_diary_api.extension import db


class Notation(db.Model):
    __tablename__ = 'notation'
    id = db.Column(db.Integer, primary_key=True)
    calendar_date = db.Column(db.Date, nullable=False)
    bedtime = db.Column(db.Time, nullable=False)
    asleep = db.Column(db.Time, nullable=False)
    awake = db.Column(db.Time, nullable=False)
    rise = db.Column(db.Time, nullable=False)
    without_sleep = db.Column(db.Time, nullable=False)
    # without_sleep = db.Column(db.Integer, nullable=False)
    # sleep_duration = db.Column(db.Integer, nullable=False)
    # time_in_bed = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True, backref=db.backref('notations', lazy=True))

    __table_args__ = (UniqueConstraint('calendar_date', 'user_id', name='uniq_calendar_date_for_user'),)

    # Todo прописать on_delete действие. При удалении пользователя - что происходит с записями дневника?
    def __repr__(self):
        return f"Запись в дневнике: [ID: {self.id}, ДАТА: {self.calendar_date}, ID ВЛАДЕЛЬЦА: {self.user_id}]"


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    date_of_registration = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"Пользователь [ID: {self.login}, LOGIN: {self.login}]"
