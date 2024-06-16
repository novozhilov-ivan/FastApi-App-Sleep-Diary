from pydantic_settings import SettingsConfigDict

from api.config import (
    FlaskConfig,
    FlaskSQLAlchemyConfig,
    PostgresDBConfig,
    SQLAlchemyConfig,
)

test_settings_config_dict = SettingsConfigDict(
    extra="ignore",
    env_file=(
        "example_test_app.env",
        "test_app.env",
    ),
    case_sensitive=False,
)


class TestFlaskConfig(FlaskConfig):
    model_config = test_settings_config_dict
    DEBUG: bool = True
    TESTING: bool = True


class TestFlaskSQLAlchemyConfig(FlaskSQLAlchemyConfig):
    model_config = test_settings_config_dict


class TestSQLAlchemyConfig(SQLAlchemyConfig):
    model_config = test_settings_config_dict


class TestPostgresDBConfig(PostgresDBConfig):
    model_config = test_settings_config_dict
    model_config["env_prefix"] = "db_"


test_sqlalchemy_config = TestSQLAlchemyConfig(
    db_config=TestPostgresDBConfig(),
)
test_flask_sqlalchemy_config = TestFlaskSQLAlchemyConfig(
    SQLALCHEMY_DATABASE_URI=test_sqlalchemy_config.database_uri,
    SQLALCHEMY_ECHO=True,
)
test_flask_config = TestFlaskConfig()
