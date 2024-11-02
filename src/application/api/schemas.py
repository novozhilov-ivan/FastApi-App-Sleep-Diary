from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel


jwt_dependency = OAuth2PasswordBearer(tokenUrl="/auth/login/")


class ErrorSchema(BaseModel):
    error: str
