from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.orm.mixins import MetaInfo


class UserORM(MetaInfo):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(128), unique=True)
    password: Mapped[bytes]
