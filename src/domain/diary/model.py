import abc

from pydantic import BaseModel

from src.domain.week.base import WeekBase


class DiaryBase(BaseModel, abc.ABC):
    weeks: list[WeekBase]


class Diary(DiaryBase):
    ...  # fmt: skip
