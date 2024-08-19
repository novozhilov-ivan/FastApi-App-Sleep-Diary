from pydantic import Field
from pydantic_settings import BaseSettings


class FlaskSettings(BaseSettings):
    DEBUG: bool = Field(
        default=False,
        title="Режим отладки",
        description=(
            "Режим отладки для просмотра ошибок."
            "Эффект от назначения этого параметра есть только когда приложение "
            "запускается через app.run()."
        ),
    )
    SECRET_KEY: str
    MAX_CONTENT_LENGTH: int = 1024 * 1024
    STATIC_FOLDER: str = "static"
    TEMPLATES_FOLDER: str = "templates"
