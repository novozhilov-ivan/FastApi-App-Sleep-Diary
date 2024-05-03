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
