from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from api.config import (
    DBConfigBase,
    FlaskSQLAlchemyConfig,
    SQLAlchemyConfig,
)

test_settings_config_dict = SettingsConfigDict(
    extra="ignore",
    env_file=".env",
    case_sensitive=False,
)


class TestFlaskConfig(BaseSettings):
    model_config = test_settings_config_dict
    DEBUG: bool = True
    TESTING: bool


class TestFlaskSQLAlchemyConfig(FlaskSQLAlchemyConfig):
    model_config = test_settings_config_dict


class TestPostgresDBConfig(DBConfigBase):
    model_config = test_settings_config_dict
    model_config["env_prefix"] = "test_db_"
    driver: str
    driver_extension: str
    user: str
    password: str
    host: str
    port: str
    name: str

    @computed_field(
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


class TestSQLAlchemyConfig(SQLAlchemyConfig):
    model_config = test_settings_config_dict


db_config = TestPostgresDBConfig()
test_sqlalchemy_config = TestSQLAlchemyConfig(
    db_config=db_config,
)
test_flask_sqlalchemy_config = TestFlaskSQLAlchemyConfig(
    SQLALCHEMY_DATABASE_URI=test_sqlalchemy_config.database_uri,
    SQLALCHEMY_ECHO=test_sqlalchemy_config.echo,
)
test_flask_config = TestFlaskConfig()
