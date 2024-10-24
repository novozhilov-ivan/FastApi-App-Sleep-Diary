from dataclasses import dataclass
from typing_extensions import Self

from sqlalchemy import select

from src.domain.entities.user import UserEntity
from src.infrastructure.database import Database
from src.infrastructure.orm import ORMUser
from src.infrastructure.repository.base import BaseUserRepository


@dataclass
class ORMUserRepository(BaseUserRepository):
    database: Database

    def get_by_username(self: Self, username: str) -> UserEntity | None:
        stmt = select(ORMUser).where(ORMUser.username == username).limit(1)

        with self.database.get_session() as session:
            result = session.scalar(stmt)

        if isinstance(result, ORMUser):
            return result.to_entity()
        return None
