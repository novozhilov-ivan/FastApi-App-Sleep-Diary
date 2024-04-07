from pydantic import BaseModel


class ErrorDescription(BaseModel):
    type: str
    loc: list[str]
    msg: str


class ErrorResponse(BaseModel):
    """Ответ с информацией об ошибках."""
    errors_count: int
    message: list[ErrorDescription]
