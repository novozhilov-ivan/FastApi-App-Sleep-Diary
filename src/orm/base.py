from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


metadata = MetaData()


class BaseORM(DeclarativeBase):
    metadata = metadata
