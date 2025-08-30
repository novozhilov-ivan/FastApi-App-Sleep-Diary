from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.sleep_diary.entities.user import UserEntity
from src.gateways.postgresql.models import ORMBase
from src.gateways.postgresql.models.mixins import MixinUpdatedAt, MixinUUIDOid


class ORMUser(ORMBase, MixinUUIDOid, MixinUpdatedAt):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(128), primary_key=True, unique=True)
    password: Mapped[str]

    def to_entity(self) -> UserEntity:
        return UserEntity(
            oid=self.oid,
            username=self.username,
            password=self.password,
        )

    @classmethod
    def from_entity(cls: type["ORMUser"], user: UserEntity) -> "ORMUser":
        return cls(
            oid=user.oid,
            username=user.username,
            password=user.password,
        )
