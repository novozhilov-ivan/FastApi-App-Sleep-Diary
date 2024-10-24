from typing_extensions import Self

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.entities.user import UserEntity
from src.infrastructure.orm.base import ORMBase
from src.infrastructure.orm.mixins import MixinUpdatedAt, MixinUUIDOid


class ORMUser(ORMBase, MixinUUIDOid, MixinUpdatedAt):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(128), primary_key=True, unique=True)
    password: Mapped[bytes]

    def to_entity(self: Self) -> UserEntity:
        return UserEntity(
            oid=self.oid,
            created_at=self.created_at,
            updated_at=self.updated_at,
            username=self.username,
            password=self.password,
        )
