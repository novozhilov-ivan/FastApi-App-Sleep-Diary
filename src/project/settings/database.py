from typing_extensions import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: str
    postgres_db_url: str

    @model_validator(mode="before")
    @classmethod
    def assemble_postgres_url(
        cls: type["PostgresSettings"],
        values: dict[str, str],
    ) -> dict[str, str]:
        if values.get("postgres_db_url"):
            return values

        username = values.get("postgres_user")
        password = values.get("postgres_password")
        host = values.get("postgres_host")
        port = values.get("postgres_port")
        db_name = values.get("postgres_db")
        values["postgres_db_url"] = (
            f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"
        )

        return values

    @property
    def test_postgres_db(self: Self) -> str:
        return f"test_{self.postgres_db}"

    @property
    def test_postgres_url(self: Self) -> str:
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.test_postgres_db}"
        )
