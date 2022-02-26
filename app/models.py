from flask_login import UserMixin

from .functions import datetime
from .config import db
from sqlalchemy import UniqueConstraint, PrimaryKeyConstraint


class Notation(db.Model):
    __tablename__ = 'notation'
    id_pk = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, nullable=True)
    calendar_date = db.Column(db.Date, nullable=False)
    bedtime = db.Column(db.Time, nullable=False)
    asleep = db.Column(db.Time, nullable=False)
    awake = db.Column(db.Time, nullable=False)
    rise = db.Column(db.Time, nullable=False)
    without_sleep = db.Column(db.Integer, nullable=False)
    sleep_duration = db.Column(db.Integer, nullable=False)
    time_in_bed = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('notations', lazy=True))

    def __repr__(self):
        return '<Notation %r>' % self.calendar_date


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    date_of_registration = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id


class BadRequest(Exception):
    pass