from datetime import date
from typing import Iterable

from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError

from api.extension import db
from api.models import DreamNote


def find_all_user_notes(user_id: int) -> Iterable[DreamNote]:
    """Получает все записи пользователя и сортирует их по дате"""
    db_response = db.session.execute(
        select(
            DreamNote,
        )
        .where(
            DreamNote.user_id == user_id,
        )
        .order_by(
            DreamNote.sleep_date,
        )
    )
    return db_response.scalars().all()


def find_user_note_by_calendar_date(
    sleep_date: date,
    user_id: int,
) -> DreamNote | None:
    """Поиск записи сна пользователя по дате"""
    db_response = db.session.execute(
        select(
            DreamNote,
        )
        .where(
            DreamNote.user_id == user_id,
        )
        .where(
            DreamNote.sleep_date == sleep_date,
        )
    )
    return db_response.scalar_one_or_none()


def find_user_note_by_note_id(
    note_id: int,
    user_id: int,
) -> DreamNote | None:
    """Поиск записи сна пользователя по id записи"""
    db_response = db.session.execute(
        select(
            DreamNote,
        )
        .where(
            DreamNote.user_id == user_id,
        )
        .where(
            DreamNote.id == note_id,
        )
    )
    return db_response.scalar_one_or_none()


def delete_user_note(
    user_id: int,
    note_id: int,
) -> None:
    db.session.execute(
        delete(
            DreamNote,
        )
        .where(
            DreamNote.id == note_id,
        )
        .where(
            DreamNote.user_id == user_id,
        )
    )
    db.session.commit()


def update_user_note(
    note_id: int,
    user_id: int,
    note_values: dict,
) -> DreamNote | None:
    try:
        db.session.execute(
            update(
                DreamNote,
            )
            .where(
                DreamNote.id == note_id,
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
            DreamNote,
        ).where(
            DreamNote.user_id == user_id,
        )
    )
    db.session.commit()


def create_one_note(note: DreamNote) -> DreamNote:
    db.session.add(note)
    db.session.commit()
    db.session.refresh(note)
    return note


def create_many_notes(notes: Iterable[DreamNote]) -> None:
    db.session.add_all(notes)
    db.session.commit()
