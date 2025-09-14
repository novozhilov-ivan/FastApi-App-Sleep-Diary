from pydantic import BaseModel, model_validator

from src.infra.identity.use_cases.commands import SignInInputData, SignUpInputData


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
