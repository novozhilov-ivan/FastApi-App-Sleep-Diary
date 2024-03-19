from typing import Sequence

from sqlalchemy import select

from sleep_diary_api.Models import Notation
from sleep_diary_api.extension import db


def get_all_notations_of_user(
        user_id: int
) -> Sequence[Notation]:
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
