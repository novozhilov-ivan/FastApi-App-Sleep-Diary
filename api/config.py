from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class FlaskConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".dev.env",
    )
    FLASK_APP: str
    FLASK_ENV: str
    FLASK_DEBUG: bool
    SECRET_KEY: str
    MAX_CONTENT_LENGTH: int = 1024 * 1024
    STATIC_FOLDER: str = "static"
    TEMPLATES_FOLDER: str = "templates"


class FlaskRestxConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".dev.env",
    )
    ERROR_INCLUDE_MESSAGE: bool = False
    SWAGGER_UI_DOC_EXPANSION: Literal["none", "list", "full"] = "list"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3
    refresh_token_expire_days: int = 30


class DBConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".dev.env",
    )
    DB_DRIVER: str
    DB_EXTEND_DRIVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str


class SQLAlchemyConfig(DBConfig):
    echo: bool = Field(
        default=False,
        alias="SQLALCHEMY_ECHO",
        title="БД Эхо",
        description="Вывод всех запросов к Базе Данных в терминал",
    )

    pool_size: int = Field(
        default=5,
        alias="POOL_SIZE",
        title="Количество соединений с БД",
        description="Ограничение по количеству соединений с Базой Данных",
    )
    max_overflow: int = Field(
        default=10,
        alias="MAX_OVERFLOW",
        title="Количество дополнительных соединений к БД",
        description=(
            "Количеству дополнительных соединений с Базой Данных сверх "
            "лимита pool_size"
        ),
    )
    expire_on_commit: bool = Field(
        default=False,
        alias="EXPIRE_ON_COMMIT",
    )
    autocommit: bool = Field(
        default=False,
        alias="AUTOCOMMIT",
    )
    autoflush: bool = Field(
        default=True,
        alias="AUTOFLUSH",
    )

    @computed_field
    def database_uri(self) -> str:
        return "{}{}{}://{}:{}@{}:{}/{}".format(
            self.DB_DRIVER,
            "+" if self.DB_EXTEND_DRIVER else "",
            self.DB_EXTEND_DRIVER,
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
        )

    @computed_field
    def session_options(self) -> dict:
        return {
            "expire_on_commit": self.expire_on_commit,
            "autocommit": self.autocommit,
            "autoflush": self.autoflush,
        }

    @computed_field
    def engine_options(self) -> dict:
        return {
            "url": self.database_uri,
            "echo": self.echo,
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
        }


sqlalchemy_config = SQLAlchemyConfig()
flask_config = FlaskConfig()
flask_restx_config = FlaskRestxConfig()
auth_config: AuthJWT = AuthJWT()
