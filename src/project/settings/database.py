from typing_extensions import Self

from pydantic import model_validator
from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB_URL: str

    @model_validator(mode="before")
    @classmethod
    def assemble_postgres_url(
        cls: type["PostgresSettings"],
        values: dict[str, str],
    ) -> dict[str, str]:
        if values.get("POSTGRES_DB_URL"):
            return values

        username = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        host = values.get("POSTGRES_HOST")
        port = values.get("POSTGRES_PORT")
        db_name = values.get("POSTGRES_DB")
        values["POSTGRES_DB_URL"] = (
            f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{db_name}"
        )

        return values

    @property
    def test_postgres_db(self: Self) -> str:
        return f"test_{self.POSTGRES_DB}"

    @property
    def test_postgres_url(self: Self) -> str:
        return (
            f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.test_postgres_db}"
        )
