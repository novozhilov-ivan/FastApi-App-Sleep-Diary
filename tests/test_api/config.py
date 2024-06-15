from pydantic_settings import SettingsConfigDict

from api.config import (
    FlaskConfig,
    FlaskSQLAlchemyConfig,
    PostgresDBConfig,
    SQLAlchemyConfig,
)

test_settings_config_dict = SettingsConfigDict(
    extra="ignore",
    env_file=".test.env",
    env_prefix="db_",
    case_sensitive=False,
)


class TestPostgresDBConfig(PostgresDBConfig):
    model_config = test_settings_config_dict


class TestSQLAlchemyConfig(SQLAlchemyConfig):
    model_config = test_settings_config_dict


class TestFlaskSQLAlchemyConfig(FlaskSQLAlchemyConfig):
    pass


class TestFlaskConfig(FlaskConfig):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".test.env",
        case_sensitive=False,
    )
    DEBUG: bool = True
    TESTING: bool = True


test_sqlalchemy_config = TestSQLAlchemyConfig(
    db_config=TestPostgresDBConfig(),
)
test_flask_sqlalchemy_config = TestFlaskSQLAlchemyConfig(
    SQLALCHEMY_DATABASE_URI=test_sqlalchemy_config.database_uri,
    SQLALCHEMY_ECHO=test_sqlalchemy_config.echo,
)
test_flask_config = TestFlaskConfig()
