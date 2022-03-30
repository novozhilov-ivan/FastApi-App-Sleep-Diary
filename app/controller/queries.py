from flask_login import current_user

from app.model import *
from app.config import db


def get_user(user_id):
    return User.query.get(user_id)


def get_amount_notations_of_user():
    return db.session.query(Notation).filter_by(user_id=current_user.id).count()


def check_user(login):
    return User.query.filter_by(login=login).first()


def get_all_notations():
    return db.session.query(Notation).order_by(Notation.calendar_date).filter_by(user_id=current_user.id)


def get_notation_by_date(notation_date):
    return db.session.query(Notation).filter_by(user_id=current_user.id, calendar_date=notation_date).one()


def add_and_commit(obj):
    db.session.add(obj)
    db.session.commit()
