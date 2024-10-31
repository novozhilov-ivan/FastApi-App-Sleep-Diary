from contextlib import contextmanager
from dataclasses import InitVar, dataclass, field
from typing import Generator
from typing_extensions import Self

from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, sessionmaker


@dataclass
class Database:
    url: InitVar[str]

    _engine: Engine = field(init=False)
    _session: sessionmaker[Session] = field(init=False)

    def __post_init__(self: Self, url: str) -> None:
        self._engine = create_engine(
            url=url,
            echo=False,
        )
        self._session = sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
        )

    @contextmanager
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
