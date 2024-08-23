from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings


class DocExpansion(str, Enum):
    NONE = "none"
    LIST = "list"
    FULL = "full"


class FlaskRestXSettings(BaseSettings):
    ERROR_INCLUDE_MESSAGE: bool = False
    SWAGGER_UI_DOC_EXPANSION: DocExpansion = Field(
        default=DocExpansion.LIST,
        description="Состояние по умолчанию вкладок в swagger",
    )
