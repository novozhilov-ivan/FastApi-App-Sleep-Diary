from typing import Iterable

from sqlalchemy import select, delete

from api.models import Notation
from api.extension import db


def read_all_user_notes(user_id: int) -> Iterable[Notation]:
    """Получает все записи пользователя и сортирует их по дате"""
    db_response = db.session.execute(
        select(
            Notation
        ).where(
            Notation.user_id == user_id
        ).order_by(
            Notation.calendar_date
        )
    )
    db_response = db_response.scalars().all()
    return db_response


def delete_all_user_notes(user_id: int) -> None:
    db.session.execute(
        delete(
            Notation
        ).where(
            Notation.user_id == user_id
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
