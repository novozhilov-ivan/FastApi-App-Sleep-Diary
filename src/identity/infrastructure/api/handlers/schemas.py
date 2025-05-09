from pydantic import BaseModel, Field


class SignInRequestSchema(BaseModel):
    username: str = Field(..., example="demo_user", title="User name")
    password: str = Field(..., example="s3cr3t", title="User password")
