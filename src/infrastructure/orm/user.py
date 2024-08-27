from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.orm.base import ORMBase
from src.infrastructure.orm.mixins import MixinMetaInfo


class ORMUser(ORMBase, MixinMetaInfo):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[bytes]