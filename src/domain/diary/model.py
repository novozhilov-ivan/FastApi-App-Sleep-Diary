import abc

from pydantic import BaseModel

from src.domain.week import BaseWeekValueObject


class DiaryBase(BaseModel, abc.ABC):
    weeks: list[BaseWeekValueObject]


class Diary(DiaryBase):
    ...  # fmt: skip
