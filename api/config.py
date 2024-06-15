import abc
from pathlib import Path
from typing import Literal

from pydantic import AnyUrl, BaseModel, Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent

dev_settings_config = SettingsConfigDict(
    extra="ignore",
    env_file=".dev.env",
    case_sensitive=False,
)

echo_field = Field(
    default=False,
    title="БД Эхо",
    description="Вывод всех запросов к Базе Данных в терминал",
)


class FlaskConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".dev.env",
    )
    DEBUG: bool = Field(
        default=False,
        title="Режим отладки",
        description=(
            "Режим отладки для просмотра ошибок."
            "Эффект от назначения этого параметра есть только когда приложение "
            "запускается через app.run()."
        ),
    )
    SECRET_KEY: str = Field(
        default="No_super_secret_key_yet",
    )
    MAX_CONTENT_LENGTH: int = Field(
        default=1024 * 1024,
    )
    STATIC_FOLDER: str = Field(
        default="static",
    )
    TEMPLATES_FOLDER: str = Field(
        default="templates",
    )


class FlaskSQLAlchemyConfig(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".dev.env",
    )
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_ECHO: bool = echo_field


class FlaskRestxConfig(BaseSettings):
    model_config = dev_settings_config
    ERROR_INCLUDE_MESSAGE: bool = Field(
        default=False,
    )
    SWAGGER_UI_DOC_EXPANSION: Literal["none", "list", "full"] = Field(
        default="list",
        description="По умолчанию состояние вкладок в swagger'е",
    )


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3
    refresh_token_expire_days: int = 30


class DBConfigBase(BaseSettings, abc.ABC):

    @property
    @abc.abstractmethod
    def database_dsn(self) -> AnyUrl: ...


class PostgresDBConfig(DBConfigBase):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".dev.env",
        env_prefix="db_",
        case_sensitive=False,
    )
    driver: str
    driver_extension: str
    user: str
    password: str
    host: str
    port: str
    name: str

    @computed_field(
        examples=[
            "postgresql+psycopg2://db_user:passwd@0.0.0.0:5432" "/db_name",
        ],
        return_type=PostgresDsn,
    )
    @property
    def database_dsn(self) -> PostgresDsn:
        return "{}{}{}://{}:{}@{}:{}/{}".format(
            self.driver,
            "+" if self.driver_extension else "",
            self.driver_extension,
            self.user,
            self.password,
            self.host,
            self.port,
            self.name,
        )


class SQLAlchemyConfig(BaseSettings):
    model_config = dev_settings_config
    db_config: DBConfigBase
    echo: bool = echo_field
    pool_size: int = Field(
        default=5,
        title="Количество соединений с БД",
        description="Ограничение по количеству соединений с Базой Данных",
    )
    max_overflow: int = Field(
        default=10,
        title="Количество дополнительных соединений к БД",
        description=(
            "Количеству дополнительных соединений с Базой Данных сверх "
            "лимита pool_size"
        ),
    )
    expire_on_commit: bool = Field(
        default=False,
    )
    autocommit: bool = Field(
        default=False,
    )
    autoflush: bool = Field(
        default=True,
    )

    @computed_field(
        examples=[
            "postgresql+psycopg2://db_user:passwd@0.0.0.0:5432/db_name",
            "sqlite:///db.sqlite",
            "sqlite::memory:",
        ],
        return_type=AnyUrl,
    )
    @property
    def database_uri(self) -> AnyUrl:
        return self.db_config.database_dsn

    @computed_field(
        return_type=dict,
    )
    @property
    def session_options(self) -> dict:
        return {
            "expire_on_commit": self.expire_on_commit,
            "autocommit": self.autocommit,
            "autoflush": self.autoflush,
        }

    @computed_field(
        return_type=dict,
    )
    @property
    def engine_options(self) -> dict:
        return {
            "url": self.database_uri,
            "echo": self.echo,
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
        }


sqlalchemy_config = SQLAlchemyConfig(
    db_config=PostgresDBConfig(),
)
flask_sqlalchemy_config = FlaskSQLAlchemyConfig(
    SQLALCHEMY_DATABASE_URI=sqlalchemy_config.database_uri,
    SQLALCHEMY_ECHO=sqlalchemy_config.echo,
)
flask_config = FlaskConfig()
flask_restx_config = FlaskRestxConfig()
auth_config: AuthJWT = AuthJWT()
