from dotenv import find_dotenv, load_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

find_env = load_dotenv(find_dotenv())


class Config(BaseSettings):
    # TODO Разбить на settings'ы для каждого плагина. ДБ, ФЛАСК, жвт
    model_config = SettingsConfigDict(env_file=".dev.env", extra="allow")

    # Flask | General Config
    FLASK_APP: str
    FLASK_ENV: str
    FLASK_DEBUG: bool
    SECRET_KEY: str
    MAX_CONTENT_LENGTH: int = 1024 * 1024
    # Flask | Static Assets
    STATIC_FOLDER: str = "static"
    TEMPLATES_FOLDER: str = "templates"
    # Flask RestX | Config
    ERROR_INCLUDE_MESSAGE: bool = False
    # PyJWT | Config
    JWT_SECRET_KEY: str

    # Database values
    DB_DRIVER: str
    DB_EXTEND_DRIVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # SQLAlchemy | Config
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

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False


config = Config()
