import contextlib

from typing import Generator
from typing_extensions import Self

from pydantic import PostgresDsn
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker


class Database:
    def __init__(self: Self, url: str | PostgresDsn) -> None:
        self._engine: Engine = create_engine(
            url=str(url),
            echo=False,
        )
        self._session: sessionmaker[Session] = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    @contextlib.contextmanager
    def get_session(self: Self) -> Generator[Session, None, None]:
        session: Session = self._session()
        try:
            yield session
        except SQLAlchemyError:
            session.rollback()
            raise
        else:
            session.commit()
        finally:
            session.close()

    @property
    def engine(self: Self) -> Engine:
        return self._engine
