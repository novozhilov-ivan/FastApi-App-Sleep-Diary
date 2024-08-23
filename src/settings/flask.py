from pydantic_settings import BaseSettings


class FlaskSettings(BaseSettings):
    SECRET_KEY: str
    MAX_CONTENT_LENGTH: int = 1024 * 1024
