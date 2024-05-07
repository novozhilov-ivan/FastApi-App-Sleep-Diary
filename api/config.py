from pathlib import Path
from typing import Literal

from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class FlaskConfig(BaseSettings):
    FLASK_APP: str
    FLASK_ENV: str
    FLASK_DEBUG: bool
    SECRET_KEY: str
    MAX_CONTENT_LENGTH: int = 1024 * 1024
    STATIC_FOLDER: str = "static"
    TEMPLATES_FOLDER: str = "templates"


class FlaskRestxConfig(BaseSettings):
    ERROR_INCLUDE_MESSAGE: bool = False
    SWAGGER_UI_DOC_EXPANSION: Literal["none", "list", "full"] = "list"


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3
    refresh_token_expire_days: int = 30


class DBConfig(BaseSettings):
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    DB_DRIVER: str
    DB_EXTEND_DRIVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:  # noqa
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


class Config(FlaskConfig, FlaskRestxConfig, DBConfig):
    auth_jwt: AuthJWT = AuthJWT()
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".dev.env",
    )


config = Config()
