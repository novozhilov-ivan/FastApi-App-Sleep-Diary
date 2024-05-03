from sqlalchemy import select

from api.extension import db
from api.models import User


def read_user_by_username(username: str):
    """Получает пользователя по id"""

    db_response = db.session.execute(
        select(
            User,
        ).where(
            User.login == username,
        )
    )
    return db_response.scalar_one_or_none()
