from dataclasses import dataclass
from datetime import date
from typing_extensions import Self

from src.domain.exceptions.date_point import (
    DatePointIsoFormatException,
    DatePointTypeException,
)
from src.domain.values.base import BaseValueObject


@dataclass(frozen=True)
class DatePoint[VTI: str | date, VTO: date](BaseValueObject):
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
