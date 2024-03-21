from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv, find_dotenv

find_env = load_dotenv(find_dotenv())


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".dev.env")

    # Flask | General Config
    FLASK_APP: str
    FLASK_ENV: str
    FLASK_DEBUG: bool
    SECRET_KEY: str
    # SERVER_NAME: str = environ.get('SERVER_NAME') Нужна доп настройка чтобы работало из контейнера
    MAX_CONTENT_LENGTH: int = 1024 * 1024

    # Database values
    DB_DRIVER: str
    DB_EXTEND_DRIVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    # Database | Sqlalchemy Config
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return "{}{}{}://{}:{}@{}:{}/{}".format(
            self.DB_DRIVER,
            "+" if self.DB_EXTEND_DRIVER else '',
            self.DB_EXTEND_DRIVER,
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_HOST,
            self.DB_PORT,
            self.DB_NAME,
        )

    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # Flask | Static Assets
    STATIC_FOLDER: str = 'static'
    TEMPLATES_FOLDER: str = 'templates'

    # etc
    FLASK_HOST: str | None = None
    FLASK_PORT: str | None = None


configuration = Config()
