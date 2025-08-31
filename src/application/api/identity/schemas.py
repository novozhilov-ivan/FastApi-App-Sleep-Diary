from pydantic import BaseModel, Field, model_validator

from src.infra.identity.use_cases.commands import SignUpInputData


class SignInRequestSchema(BaseModel):
    username: str = Field(examples=["demo_user"], title="User name")
    password: str = Field(examples=["s3cr3t"], title="User password")


class SignUpRequestSchema(BaseModel):
    username: str
    plain_password_first: str
    plain_password_second: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "SignUpRequestSchema":
        if self.plain_password_first != self.plain_password_second:
            raise ValueError("Passwords do not match")
        return self

    def to_command(self) -> SignUpInputData:
        return SignUpInputData(
            username=self.username,
            plain_password_first=self.plain_password_first,
            plain_password_second=self.plain_password_second,
        )
