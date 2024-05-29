from flask_login import current_user

from app.Models import *
from app import db


def add_all_and_commit(list_of_DreamNotes: list):
    """Добавляет и сохраняет в бд все записи из получаемого списка"""
    db.session.add_all(list_of_DreamNotes)
    db.session.commit()


def check_DreamNote_availability(new_date):
    """Ищет запись в дневнике сна с получаемой датой"""
    return (
        db.session.query(DreamNote)
        .filter_by(user_id=current_user.id, calendar_date=new_date)
        .first()
    )


def delete_DreamNote_and_commit(DreamNote):
    """Удаляет одну запись из дневника и сохраняет состояние"""
    db.session.delete(DreamNote)
    db.session.commit()


def delete_all_DreamNotes():
    """Удаляет все записи из дневника и сохраняет состояние"""
    db.session.query(DreamNote).filter_by(user_id=current_user.id).delete()
    db.session.commit()


def get_user(user_id: str):
    """Получает пользователя по id"""
    return db.session.query(User).get(user_id)


def get_amount_DreamNotes_of_user():
    """Получает количество записей в дневнике пользователя"""
    return DreamNote.query.filter_by(user_id=current_user.id).count()


def check_user(login: str):
    """Проверяет существует ли такой пользователь по получаемому логину"""
    return db.session.query(User).filter_by(login=login).first()


def get_all_dates_of_user():
    return (
        db.session.query(DreamNote.calendar_date)
        .filter_by(user_id=current_user.id)
        .order_by(DreamNote.calendar_date)
        .all()
    )


def get_all_DreamNotes_of_user():
    """Получает все записи пользователя и сортирует их по дате"""
    return (
        DreamNote.query.filter_by(user_id=current_user.id)
        .order_by(DreamNote.calendar_date)
        .all()
    )


def get_DreamNote_by_date(DreamNote_date):
    """Проверяет существует ли запись пользователя с получаемой датой"""
    return (
        db.session.query(DreamNote)
        .filter_by(user_id=current_user.id, calendar_date=DreamNote_date)
        .one()
    )


def add_and_commit(obj):
    """Добавляет одну запись в дневник и сохраняет состояние"""
    db.session.add(obj)
    db.session.commit()
