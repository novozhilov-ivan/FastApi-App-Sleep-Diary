from dataclasses import dataclass

from sqlalchemy import select

from src.domain.sleep_diary.entities.user import UserEntity
from src.domain.sleep_diary.services.base import IUsersRepository
from src.gateways.postresql.database import Database
from src.gateways.postresql.models import ORMUser


@dataclass
class ORMUsersRepository(IUsersRepository):
    database: Database

    def get_by_username(self, username: str) -> UserEntity | None:
        stmt = select(ORMUser).where(ORMUser.username == username).limit(1)

        with self.database.get_session() as session:
            result = session.scalar(stmt)

        if isinstance(result, ORMUser):
            return result.to_entity()
        return None

    def add_user(self, user: UserEntity) -> None:
        with self.database.get_session() as session:
            session.add(ORMUser.from_entity(user))

    def delete_user(self, username: str) -> None:
        pass
