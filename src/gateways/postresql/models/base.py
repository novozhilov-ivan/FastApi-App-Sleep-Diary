from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase


metadata = MetaData()


class ORMBase(DeclarativeBase):
    metadata = metadata
