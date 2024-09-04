from typing import ClassVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
)

from src.pydantic_schemas.sleep.weeks import (
    SleepDiaryWeekCompute,
    SleepDiaryWeekModel,
)


class SleepDiaryStatisticModel(BaseModel):
    notes_count: int
    weeks_count: int


class SleepDiaryDataModel(BaseModel):
    weeks: list[SleepDiaryWeekModel]


class SleepDiaryModel(SleepDiaryDataModel, SleepDiaryStatisticModel):
    """Дневника сна пользователя с записями и информацией о количестве записей"""

    model_config: ClassVar[ConfigDict] = ConfigDict(from_attributes=True)


class SleepDiaryModelEmpty(SleepDiaryModel):
    """Дневника сна без записей"""

    notes_count: int = 0
    weeks_count: int = 0
    weeks: list = Field(default_factory=list)


class SleepDiaryDataCompute(BaseModel):
    weeks: list[SleepDiaryWeekCompute]


class SleepDiaryCompute(SleepDiaryDataCompute):
    @computed_field  # type: ignore[misc]
    @property
    def notes_count(self) -> int:
        if not self.weeks:
            return 0
        days_in_weeks = map(lambda week: len(week.notes), self.weeks)
        return sum(days_in_weeks)

    @computed_field  # type: ignore[misc]
    @property
    def weeks_count(self) -> int:
        return len(self.weeks)
