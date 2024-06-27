from datetime import date
from typing import Iterable

import sqlalchemy
from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError

from src.extension import db
from src.models import SleepNoteOrm


def find_all_user_notes(user_id: int) -> Iterable[SleepNoteOrm]:
    """Получает все записи пользователя и сортирует их по дате"""
    db_response = db.session.execute(
        select(SleepNoteOrm)
        .where(SleepNoteOrm.owner_id == user_id)
        .order_by(SleepNoteOrm.sleep_date)
    )
    return db_response.scalars().all()


def find_user_note_by_calendar_date(
    sleep_date: date,
    user_id: int,
) -> SleepNoteOrm | None:
    """Поиск записи сна пользователя по дате"""
    db_response = db.session.execute(
        select(SleepNoteOrm)
        .where(SleepNoteOrm.owner_id == user_id)
        .where(SleepNoteOrm.sleep_date == sleep_date)
    )
    return db_response.scalar_one_or_none()


def find_user_note_by_note_id(id: int, user_id: int) -> SleepNoteOrm | None:
    """Поиск записи сна пользователя по id записи"""
    db_response = db.session.execute(
        select(SleepNoteOrm)
        .where(SleepNoteOrm.owner_id == user_id)
        .where(SleepNoteOrm.id == id)
    )
    return db_response.scalar_one_or_none()


def delete_user_note(id: int, user_id: int) -> None:
    db.session.execute(
        delete(SleepNoteOrm)
        .where(SleepNoteOrm.owner_id == user_id)
        .where(SleepNoteOrm.id == id)
    )
    db.session.commit()


def update_user_note(
    id: int,
    user_id: int,
    note_values: dict,
) -> SleepNoteOrm | None:
    try:
        db.session.execute(
            update(SleepNoteOrm).where(SleepNoteOrm.id == id).values(note_values)
        )
        db.session.commit()
    except SQLAlchemyError:
        return None
    else:
        return find_user_note_by_note_id(
            id=id,
            user_id=user_id,
        )


def delete_all_user_notes(user_id: int) -> None:
    db.session.execute(delete(SleepNoteOrm).where(SleepNoteOrm.owner_id == user_id))
    db.session.commit()


def create_one_note(note: SleepNoteOrm) -> SleepNoteOrm:
    db.session.add(note)
    db.session.commit()
    db.session.refresh(note)
    return note


def create_many_notes(notes: Iterable[SleepNoteOrm]) -> bool:
    try:
        db.session.add_all(notes)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return False
    else:
        return True
