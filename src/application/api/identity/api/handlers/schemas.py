from pydantic import BaseModel, Field


class SignInRequestSchema(BaseModel):
    username: str = Field(examples=["demo_user"], title="User name")
    password: str = Field(examples=["s3cr3t"], title="User password")
