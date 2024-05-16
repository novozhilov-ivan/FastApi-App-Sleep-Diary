from datetime import date
from typing import Iterable

from sqlalchemy import delete, select

from api.extension import db
from api.models import Notation


def read_all_user_notes(user_id: int) -> Iterable[Notation]:
    """Получает все записи пользователя и сортирует их по дате"""
    db_response = db.session.execute(
        select(
            Notation,
        )
        .where(
            Notation.user_id == user_id,
        )
        .order_by(
            Notation.calendar_date,
        )
    )
    return db_response.scalars().all()


def find_user_note_by_calendar_date(
    calendar_date: date,
    user_id: int,
) -> Notation | None:
    """Поиск записи сна пользователя по дате"""
    db_response = db.session.execute(
        select(
            Notation,
        )
        .where(
            Notation.user_id == user_id,
        )
        .where(
            Notation.calendar_date == calendar_date,
        )
    )
    return db_response.scalar_one_or_none()


def delete_all_user_notes(user_id: int) -> None:
    db.session.execute(
        delete(
            Notation,
        ).where(
            Notation.user_id == user_id,
        )
    )
    db.session.commit()


def create_one_note(note: Notation) -> Notation:
    db.session.add(note)
    db.session.commit()
    db.session.refresh(note)
    return note


def create_many_notes(notes: Iterable[Notation]) -> None:
    db.session.add_all(notes)
    db.session.commit()
