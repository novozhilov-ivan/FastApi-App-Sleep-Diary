from pydantic import model_validator
from typing_extensions import Self

from src.domain.note.base import NoteBase
from src.domain.note.error import ValidateSleepTimePointError


class NoteWithFieldsValidator(NoteBase):
    @model_validator(mode="after")
    def validate_time_points_sequences(self) -> Self:
        if (
            self.went_to_bed <= self.fell_asleep <= self.woke_up <= self.got_up
            or self.got_up <= self.went_to_bed <= self.fell_asleep <= self.woke_up
            or self.woke_up <= self.got_up <= self.went_to_bed <= self.fell_asleep
            or self.fell_asleep <= self.woke_up <= self.got_up <= self.went_to_bed
        ):
            return self
        raise ValidateSleepTimePointError
