from dataclasses import dataclass
from datetime import date
from typing_extensions import Self

from src.domain.exceptions import (
    DatePointIsoFormatException,
    DatePointTypeException,
)
from src.domain.values.base import BaseDateTimeValueObject


@dataclass(frozen=True)
class DatePoint[VTDI: str | date, VTDO: date](BaseDateTimeValueObject):
    def validate(self: Self) -> None:
        if not isinstance(self.value, (date, str)):
            raise DatePointTypeException

        if isinstance(self.value, str):
            try:
                date.fromisoformat(self.value)
            except ValueError:
                raise DatePointIsoFormatException

    def as_generic_type(self: Self) -> date:
        if isinstance(self.value, str):
            return date.fromisoformat(self.value)
        return date(self.value.year, self.value.month, self.value.day)
