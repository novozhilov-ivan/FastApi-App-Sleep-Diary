from typing import Sequence

from sqlalchemy import select

from api.models import Notation
from api.extension import db


def get_all_notations_of_user(user_id: int) -> Sequence[Notation]:
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


def post_new_note(new_note: Notation) -> Notation:
    db.session.add(new_note)
    db.session.commit()
    db.session.refresh(new_note)
    return new_note

