from typing import ClassVar

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgreSQLSettings(BaseSettings):
    _env_prefix: ClassVar[str] = "POSTGRES_"

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_prefix=_env_prefix,
        case_sensitive=False,
        env_file=".env",
        extra="ignore",
    )

    db: str
    user: str
    password: str
    host: str
    port: str
    db_url: str

    @model_validator(mode="before")
    @classmethod
    def assemble_postgres_url(cls, values: dict[str, str]) -> dict[str, str]:
        if values.get("db_url"):
            return values

        username = values.get("user")
        password = values.get("password")
        host = values.get("host")
        port = values.get("port")
        db_name = values.get("db")
        values["db_url"] = (
            f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"
        )

        return values

    @property
    def test_db(self) -> str:
        return f"test_{self.db}"

    @property
    def test_url(self) -> str:
        return (
            f"postgresql+psycopg2://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.test_db}"
        )
