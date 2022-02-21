from flask_login import UserMixin

from .functions import datetime
from app import db, login_manager


class Notation(db.Model):
    id = db.Column(db.Integer, nullable=True)
    # user_id = db.Column(db.INT, db.ForeignKey('user.id'), nullable=False)
    # user = db.relationship('User', backref=db.backref('', lazy=True))
    calendar_date = db.Column(db.Date, primary_key=True)
    bedtime = db.Column(db.Time, nullable=False)
    asleep = db.Column(db.Time, nullable=False)
    awake = db.Column(db.Time, nullable=False)
    rise = db.Column(db.Time, nullable=False)
    without_sleep = db.Column(db.INT, nullable=False)
    sleep_duration = db.Column(db.INT, nullable=False)
    time_in_bed = db.Column(db.INT, nullable=False)

    def __repr__(self):
        return '<Notation %r>' % self.calendar_date


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    date_of_registration = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.login


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
