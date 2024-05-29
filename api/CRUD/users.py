from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError

from api.extension import db
from api.models import User


def read_user_by_username(username: str) -> User | None:
    """Получает пользователя по username"""

    db_response = db.session.execute(
        select(
            User,
        ).where(
            User.username == username,
        )
    )
    db.session.commit()
    return db_response.scalar_one_or_none()


def find_user_by_id(user_id: int) -> User | None:
    """Получает пользователя по id"""

    db_response = db.session.execute(
        select(
            User,
        ).where(
            User.id == user_id,
        )
    )
    return db_response.scalar_one_or_none()


def delete_user_by_id(user_id: int) -> None:
    """Удалить пользователя"""
    db.session.execute(
        delete(
            User,
        ).where(
            User.id == user_id,
        )
    )


def create_new_user_by_username(user: User) -> User | None:
    """Создать нового пользователя"""
    try:
        db.session.add(user)
        db.session.commit()
    except SQLAlchemyError:
        return None
    else:
        db.session.refresh(user)
        return user
