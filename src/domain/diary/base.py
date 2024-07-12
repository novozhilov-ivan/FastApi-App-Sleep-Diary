import abc

from typing import ClassVar
from typing_extensions import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    computed_field,
)

from src.domain import week as wk


class BaseDiary(BaseModel, abc.ABC):
    @computed_field  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def notes_count(self: Self) -> int: ...

    @computed_field  # type: ignore[misc]
    @property
    @abc.abstractmethod
    def weeks_count(self: Self) -> int: ...

    weeks: list[wk.BaseWeek] = Field(
        default_factory=list,
        validate_default=False,
        min_length=1,
    )
    model_config: ClassVar[ConfigDict] = ConfigDict(arbitrary_types_allowed=True)
