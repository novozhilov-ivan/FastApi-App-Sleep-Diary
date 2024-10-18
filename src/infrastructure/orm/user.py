from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.orm.base import ORMBase
from src.infrastructure.orm.mixins import MixinUpdatedAt, MixinUUIDOid


class ORMUser(ORMBase, MixinUUIDOid, MixinUpdatedAt):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(128), primary_key=True, unique=True)
    password: Mapped[bytes]
