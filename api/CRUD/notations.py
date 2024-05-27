from datetime import date
from typing import Iterable

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError

from api.extension import db
from api.models import Notation


def find_all_user_notes(user_id: int) -> Iterable[Notation]:
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


def find_user_note_by_note_id(
    note_id: int,
    user_id: int,
) -> Notation | None:
    """Поиск записи сна пользователя по id записи"""
    db_response = db.session.execute(
        select(
            Notation,
        )
        .where(
            Notation.user_id == user_id,
        )
        .where(
            Notation.id == note_id,
        )
    )
    return db_response.scalar_one_or_none()


def delete_user_note(
    user_id: int,
    note_id: int,
) -> None:
    db.session.execute(
        delete(
            Notation,
        )
        .where(
            Notation.id == note_id,
        )
        .where(
            Notation.user_id == user_id,
        )
    )
    db.session.commit()


def update_user_note(
    note_id: int,
    user_id: int,
    note_values: dict,
) -> Notation | None:
    try:
        db.session.execute(
            update(
                Notation,
            )
            .where(
                Notation.id == note_id,
            )
            .values(note_values)
        )
        db.session.commit()
    except SQLAlchemyError:
        return None
    else:
        return find_user_note_by_note_id(
            note_id=note_id,
            user_id=user_id,
        )


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
