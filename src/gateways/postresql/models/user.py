from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.sleep_diary.entities.user import UserEntity
from src.gateways.postresql.models import ORMBase
from src.gateways.postresql.models.mixins import MixinUpdatedAt, MixinUUIDOid


class ORMUser(ORMBase, MixinUUIDOid, MixinUpdatedAt):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(128), primary_key=True, unique=True)
    password: Mapped[str]

    def to_entity(self) -> UserEntity:
        return UserEntity(
            oid=self.oid,
            created_at=self.created_at,
            updated_at=self.updated_at,
            username=self.username,
            password=self.password,
        )

    @classmethod
    def from_entity(cls: type["ORMUser"], user: UserEntity) -> "ORMUser":
        return cls(
            oid=user.oid,
            created_at=user.created_at,
            updated_at=user.updated_at,
            username=user.username,
            password=user.password,
        )
