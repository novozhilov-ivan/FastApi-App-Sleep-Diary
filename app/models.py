# from flask_login import UserMixin

from app import db


class Notation(db.Model):
    id = db.Column(db.Integer, nullable=True)
    calendar_date = db.Column(db.Date, primary_key=True)
    bedtime = db.Column(db.Time, nullable=False)
    asleep = db.Column(db.Time, nullable=False)
    awake = db.Column(db.Time, nullable=False)
    rise = db.Column(db.Time, nullable=False)
    without_sleep = db.Column(db.INT, nullable=False)
    sleep_duration = db.Column(db.INT, nullable=False)
    time_in_bed = db.Column(db.INT, nullable=False)

    def __repr__(self):
        return '<Notation %r>' % self.id


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     login = db.Column(db.String(128), nullable=False, unique=True)
#     password = db.Column(db.String(128), nullable=False)
