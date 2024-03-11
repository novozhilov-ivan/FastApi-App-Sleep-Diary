from flask_login import current_user

from app.models import *
from app import db


def add_all_and_commit(list_of_notations: list):
    """Добавляет и сохраняет в бд все записи из получаемого списка"""
    db.session.add_all(list_of_notations)
    db.session.commit()


def check_notation_availability(new_date):
    """Ищет запись в дневнике сна с получаемой датой"""
    return db.session.query(Notation).filter_by(user_id=current_user.id, calendar_date=new_date).first()


def delete_notation_and_commit(notation):
    """Удаляет одну запись из дневника и сохраняет состояние"""
    db.session.delete(notation)
    db.session.commit()


def delete_all_notations():
    """Удаляет все записи из дневника и сохраняет состояние"""
    db.session.query(Notation).filter_by(user_id=current_user.id).delete()
    db.session.commit()


def get_user(user_id: str):
    """Получает пользователя по id"""
    return db.session.query(User).get(user_id)


def get_amount_notations_of_user():
    """Получает количество записей в дневнике пользователя"""
    return Notation.query.filter_by(user_id=current_user.id).count()


def check_user(login: str):
    """Проверяет существует ли такой пользователь по получаемому логину"""
    return db.session.query(User).filter_by(login=login).first()


def get_all_dates_of_user():
    return db.session.query(
        Notation.calendar_date
    ).filter_by(user_id=current_user.id).order_by(Notation.calendar_date).all()


def get_all_notations_of_user():
    """Получает все записи пользователя и сортирует их по дате"""
    return Notation.query.filter_by(user_id=current_user.id).order_by(Notation.calendar_date).all()


def get_notation_by_date(notation_date):
    """Проверяет существует ли запись пользователя с получаемой датой"""
    return db.session.query(Notation).filter_by(user_id=current_user.id, calendar_date=notation_date).one()


def add_and_commit(obj):
    """Добавляет одну запись в дневник и сохраняет состояние"""
    db.session.add(obj)
    db.session.commit()
