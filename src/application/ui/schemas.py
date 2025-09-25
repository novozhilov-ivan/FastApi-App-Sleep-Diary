from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, model_validator

from src.infra.identity.use_cases.commands import SignInInputData, SignUpInputData
from src.infra.sleep_diary.commands import EditNoteCommand


class MakeSignUpSchema(BaseModel):
    username: str
    plain_password_first: str
    plain_password_second: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "MakeSignUpSchema":
        if self.plain_password_first != self.plain_password_second:
            raise ValueError("Пароли не совпадают")
        return self

    def to_command(self) -> SignUpInputData:
        return SignUpInputData(
            username=self.username,
            plain_password_first=self.plain_password_first,
            plain_password_second=self.plain_password_second,
        )


class MakeSignInSchema(BaseModel):
    username: str
    password: str

    def to_command(self) -> SignInInputData:
        return SignInInputData(username=self.username, password=self.password)


class CreateNoteSchema(BaseModel):
    bedtime_date: date
    went_to_bed: time
    fell_asleep: time
    woke_up: time
    got_up: time
    no_sleep: time = time()


class PatchNoteSchema(BaseModel):
    went_to_bed: time | None = None
    fell_asleep: time | None = None
    woke_up: time | None = None
    got_up: time | None = None
    no_sleep: time | None = None

    def to_command(self, owner_oid: UUID, note_date: date) -> EditNoteCommand:
        return EditNoteCommand(
            owner_oid=owner_oid,
            note_date=note_date,
            went_to_bed=self.went_to_bed,
            fell_asleep=self.fell_asleep,
            woke_up=self.woke_up,
            got_up=self.got_up,
            no_sleep=self.no_sleep,
        )
