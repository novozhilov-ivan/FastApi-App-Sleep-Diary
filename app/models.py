from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)
# Создание бд:
# from app import db
# db.create_all()


class Notation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calendar_date = db.Column(db.Date, nullable=False)
    bedtime = db.Column(db.Time, nullable=False)
    asleep = db.Column(db.Time, nullable=False)
    awake = db.Column(db.Time, nullable=False)
    rise = db.Column(db.Time, nullable=False)
    without_sleep = db.Column(db.INT, nullable=False)
    sleep_duration = db.Column(db.INT, nullable=False)
    time_in_bed = db.Column(db.INT, nullable=False)

    def __repr__(self):
        return '<Notation %r>' % self.id
