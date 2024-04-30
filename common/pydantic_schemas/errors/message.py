from pydantic import BaseModel, computed_field


class ErrorDescription(BaseModel):
    type: str
    loc: list[str]
    msg: str


class ErrorResponse(BaseModel):
    """Ответ с информацией об ошибках"""

    message: list[ErrorDescription] | str

    @computed_field
    @property
    def errors_count(self) -> int:
        if isinstance(self.message, list):
            return len(self.message)
        return 1
